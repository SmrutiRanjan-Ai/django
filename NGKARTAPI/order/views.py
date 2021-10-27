from django.shortcuts import render
from django.http import Http404
from django.http.response import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.files.storage import default_storage
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.parsers import JSONParser
from rest_framework import status, permissions
from rest_framework.serializers import Serializer
from rest_framework.views import APIView
from product.serializers import ProductSerializer
from order.models import *
from order.serializers import *
from permission.views import StaffPermission, OrderPostPermission, ObjectLevelOrderGetPermission
from rest_framework.authentication import TokenAuthentication
# Create your views here.

class OrderViewList(APIView, OrderPostPermission):
    """
        Inhereits APIView class to encapsulate Read(GET) and Create(POST) operations on
        the model/table Order
    """
    authentication_classes = (TokenAuthentication,)
    permission_classes = [OrderPostPermission]

    def validate_order(self, request):

        error_message = {}
        total_order_cost = 0
        item_count = 0

        if 'OrderItems' not in request.data:
            error_message['order'] = ['Key OrderItems not found']
            return (request.data, None, error_message)

        order_items = request.data['OrderItems']
        if len(order_items) == 0:
            error_message['order'] = ['No item found']

        for item in order_items:

            product = None
            product_cost = 0
            productId = None
            error_message[item_count] = []

            if 'ProductId' not in item:
                error_message[item_count].append('Missing product id for this item')
            else:
                item['ProductId'] = int(item['ProductId'])
                productId = item['ProductId']
                try:
                    product = Product.objects.get(ProductId=productId)
                except Product.DoesNotExist:
                    error_message[item_count].append('Product with id '+str(productId)+' doesnt exist')

            if 'ProductQuantity' in item:
                item['ProductQuantity'] = int(item['ProductQuantity'])
                productQuantity = item['ProductQuantity']
                if product is not None:
                    if product.ProductInventory < productQuantity:
                        error_message[item_count].append('Product with id '+str(productId)+' has only '+str(product.ProductInventory)+' items left')
                    else:
                        product_cost = product.ProductFeaturedPrice * productQuantity
                        product_cost -= (product_cost * product.ProductDiscountPercentage)/100
                        product_cost += (product_cost * product.ProductShippingRate)/100

                        tax = product.ProductTaxCode
                        if tax is not None:
                            product_cost += (product_cost * tax.TaxRate)/100
                        item['ProductTotalCost'] = product_cost
            else:
                error_message[item_count].append('Missing product quantity for this item')

            total_order_cost += product_cost

            if len(error_message[item_count]) == 0:
                del error_message[item_count]
            item_count += 1

        if 'OrderShippingRate' in request.data:
            total_order_cost += (total_order_cost * request.data['OrderShippingRate'])/100
        total_order_cost = round(total_order_cost, 2)

        request.data['OrderTotal'] = total_order_cost
        return (request.data, request.data['OrderItems'], error_message)


    def get(self, request, format=None):
        """
            Returns all instances of the table Order

            :param request: Request object
            :param format: Format of the input. Default is JSON
            :return: Response object with serialized data corrsponding to all order instances
        """
        print(request.method)
        orders = Order.objects.all()
        serializer = OrderSerializer(orders, many=True)
        return Response(serializer.data)


    def post(self, request, format=None):
        """
            Saves the data accompanied by the request as an new instance
            in the Order table if its valid.

            :param request: Request object
            :param format: Format of the input. Default is JSON
            :return: Response object with serialized data corrsponding to added order instance
        """
        res = self.validate_order(request)
        if len(res[2]) > 0:
            return Response({'status' : 'false', 'message' : res[2]}, status=status.HTTP_400_BAD_REQUEST)

        serializer = OrderSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            order_item_view = OrderItemViewListForOrderId()
            response = order_item_view.save_order_items(request.data['OrderItems'], serializer.data['OrderId'])
            if response.data['status'] == 'false':
                return response
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class OrderViewForId(APIView, ObjectLevelOrderGetPermission):
    """
        Inhereits APIView class to encapsulate Read(GET), Update(PUT) and Delete(DELETE)
        operations on the model/table Order
    """
    authentication_classes = (TokenAuthentication,)
    permission_classes = [ObjectLevelOrderGetPermission]

    def get_order(self, id):
        """
            Fetch an instance based on its primary key ie orderId from the Order table
            If no id is found return None

            :param id: Id of the instance which needs to be fetched
            :return: Order instance with given id.
                        If not found returns None
        """
        try:
            return Order.objects.get(OrderId=id)
        except Order.DoesNotExist:
            self.NOT_FOUND_RESP = Response(
                        {
                            "status" : "false",
                            "message" : "Couldn't find order "+str(id)
                        },
                        status=status.HTTP_404_NOT_FOUND)
            return None

    def get(self, request, id, format=None):
        """
            Fetch an instance based on its primary key ie orderId from the Order table.
            If no id is found return JSONResponse with Order Not Found message.

            :param id: Id of the instance which needs to be fetched
            :return: Order instance with given id.
                    If not found returns JSONResponse
        """
        order = self.get_order(id)
        if order is None:
            return self.NOT_FOUND_RESP
        serializer = OrderSerializer(order)
        return Response(serializer.data)


    def put(self, request, id, format=None):

        id = int(id)
        order = self.get_order(id)
        if order is None:
            return self.NOT_FOUND_RESP

        if 'OrderId' in request.data and request.data['OrderId'] != id:
            return Response(
                        {
                            "status" : "false",
                            "message" : "OrderId mismatch"
                        },
                        status=status.HTTP_400_BAD_REQUEST)

        if 'OrderId' not in request.data:
            request.data['OrderId'] = id

        serializer = OrderSerializer(order, data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_202_ACCEPTED)


    def delete_order_items(self, orderId):
        order_items = OrderItem.objects.filter(OrderId=orderId)
        if order_items is None:
            return False
        for item in order_items:
            item.delete()
        return True


    def delete(self, request, id, format=None):
        orderId = int(id)
        order = None
        self.delete_order_items(orderId)
        try:
            order = Order.objects.get(OrderId=orderId)
            order.delete()
            return Response({"status" : "true", "message" : "Deleted order "+str(orderId)+" sucessfully"}, \
                            status=status.HTTTP_204_BAD_NO_CONTENT)
        except:
            return Response(
                        {
                            "status" : "false",
                            "message" : "Couldn't find order "+str(orderId)
                        },
                        status=status.HTTP_404_NOT_FOUND)


class OrderItemViewList(APIView, StaffPermission):
    """
        Inhereits APIView class to encapsulate Read(GET) operation on the model/table OrderItems
    """
    authentication_classes = (TokenAuthentication,)
    permission_classes = [StaffPermission]

    def get(self, request, format=None):
        """
            Returns all instances of the table OrderItem

            :param request: Request object
            :param format: Format of the input. Default is JSON
            :return: Response object with serialized data corrsponding to all order item instances
        """
        order_items = OrderItem.objects.all()
        serializer = OrderItemSerializer(order_items, many=True)
        return Response(serializer.data)


class OrderItemViewListForOrderId(APIView, StaffPermission):
    """
        Inhereits APIView class to encapsulate Read(GET) and Create(POST) operations
        on the model/table OrderItems
    """
    authentication_classes = (TokenAuthentication,)
    permission_classes = (permissions.AllowAny,)

    def get(self, request, orderId, format=None):
        """
            Returns all instances of the table OrderItem for given orderId

            :param request: Request object
            :param format: Format of the input. Default is JSON
            :return: Response object with serialized data corrsponding to all order item instances
        """
        try:
            order_items = OrderItem.objects.filter(OrderId=orderId)
            if order_items is None:
                raise OrderItem.DoesNotExist
            serializer = OrderItemSerializer(order_items, many=True)
            return Response({
                                'OrderItems' : serializer.data,
                                'status' : 'true',
                            })
        except OrderItem.DoesNotExist:
            return Response(
                        {
                            "status" : "false",
                            "message" : "Couldn't find order items for the order "+str(orderId)
                        },
                        status=status.HTTP_404_NOT_FOUND)


    def save_order_items(self, order_items, orderId):
        """
            Creates all instances for given orderId in OrderItem table

            :param request: Request object
            :param format: Format of the input. Default is JSON
            :return: Response object with serialized data corrsponding to all order item instances
        """
        order_view_for_id = OrderViewForId()
        order = order_view_for_id.get_order(orderId)
        if order is None:
            return order_view_for_id.NOT_FOUND_RESP

        try:
            OrderItem.objects.get(OrderId=orderId)
            return Response({
                            'status':'false',
                            'message':'Order Items for following order exist already. POST request not allowed'
                            }, status=status.HTTP_400_BAD_REQUEST)
        except OrderItem.DoesNotExist:
            pass

        errors = None
        for order_item in order_items:
            order_item['OrderId'] = orderId
            order_item_serializer = OrderItemSerializer(data=order_item)
            if order_item_serializer.is_valid():
                order_item_serializer.save()
            else:
                errors = order_item_serializer.errors
                break

        if errors is not None:
            return Response({
                            'status':'false',
                            'message':'Error encountered while saving order items',
                            'errors' : errors
                            }, status=status.HTTP_400_BAD_REQUEST)

        return Response({
                        'status':'true',
                        'message':'Found order and upated order items'
                        }, status=status.HTTP_202_ACCEPTED)


    def delete(self, request, orderId, format=None):
        order_view_for_id = OrderViewForId()
        result = order_view_for_id.delete_order_items(orderId)
        message = "Deleted order items for order "+str(orderId)+" sucessfully"

        if not result:
            message = "No items found for order "+str(orderId)

        return Response({
                        "status" : str(result),
                        "message" : message
                        }, \
                        status=status.HTTTP_204_BAD_NO_CONTENT)


class OrderItemCreateReadUpdateView(APIView, StaffPermission):
    permission_classes = [StaffPermission]

    def get(self, request, orderId, format=None):
        order_view_for_id = OrderViewForId()
        order = order_view_for_id.get_order(orderId)
        if order is None:
            return order_view_for_id.NOT_FOUND_RESP

        order_items = OrderItem.objects.filter(OrderId=orderId)
        serializer = OrderItemSerializer(order_items, many=True)

        return Response({
                        'status':'true',
                        'OrderItems' : serializer.data
                        })

    def put(self, request, orderId, format=None):

        orderId = int(orderId)
        order_view_for_id = OrderViewForId()
        order = order_view_for_id.get_order(orderId)
        if order is None:
            return order_view_for_id.NOT_FOUND_RESP

        serializer = OrderItemSerializer(data=request.data)

        if not serializer.is_valid():
            return Response({
                            'status':'false',
                            'errors': serializer.errors
                            }, status=status.HTTP_400_BAD_REQUEST)

        if serializer.data['OrderId'] != orderId:
            return Response({
                    'status':'false',
                    'message':'OrderId mismatch'
                    }, status=status.HTTP_400_BAD_REQUEST)

        order_item = None
        try:
            order_item = OrderItem.objects.filter(OrderId=orderId).get(ProductId=serializer.data['ProductId'])
        except OrderItem.DoesNotExist:
            return Response({
                        'status':'false',
                        'message':'Product not found with id '+str(serializer.data['ProductId'])
                        }, status=status.HTTP_404_NOT_FOUND)

        product = Product.objects.get(ProductId=serializer.data['ProductId'])
        quantity_required = request.data['ProductQuantity']-order_item.ProductQuantity

        if product.ProductInventory < quantity_required:
            return Response({
                        'status':'false',
                        'message':'Insufficient products in the inventory for productId: '+str(product.ProductId)
                        }, status=status.HTTP_400_BAD_REQUEST)

        product.ProductInventory -= quantity_required

        request.data['ProductTotalCost'] = round(request.data['ProductQuantity']*product.ProductFeaturedPrice,2)
        serializer = OrderItemSerializer(order_item, data=request.data)

        if not serializer.is_valid():
            return Response({
                'status':'false',
                'errors': serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)

        serializer.save()
        product.save()

        return Response({
                        'status':'true',
                        'message':'Found and upated order item'
                        }, status=status.HTTP_202_ACCEPTED)


    def post(self, request, orderId, format=None):
        orderId = int(orderId)
        order_view_for_id = OrderViewForId()
        order = order_view_for_id.get_order(orderId)
        if order is None:
            return order_view_for_id.NOT_FOUND_RESP

        serializer = OrderItemSerializer(data=request.data)
        if not serializer.is_valid():
            return Response({
                            'status':'false',
                            'errors': serializer.errors
                            }, status=status.HTTP_400_BAD_REQUEST)

        if serializer.data['OrderId'] != orderId:
            return Response({
                    'status':'false',
                    'message':'OrderId mismatch'
                    }, status=status.HTTP_400_BAD_REQUEST)

        productId = serializer.data['ProductId']
        try:
            OrderItem.objects.get(OrderId=orderId, ProductId=productId)
            return Response({
                        'status':'false',
                        'message':'Order item with given ProductId: '+str(productId)+' already exists'
                        }, status=status.HTTP_400_BAD_REQUEST)
        except OrderItem.DoesNotExist:
            pass

        product = Product.objects.get(ProductId=productId)
        product_serializer = ProductSerializer(product)
        if product_serializer.data['ProductInventory'] < serializer.data['ProductQuantity']:
            return Response({
                        'status':'false',
                        'message':'Insufficient products in the inventory for productId: '+str(productId)
                        }, status=status.HTTP_400_BAD_REQUEST)

        request.data['ProductTotalCost'] = round(serializer.data['ProductQuantity']*\
                                                product_serializer.data['ProductFeaturedPrice'],2)
        serializer = OrderItemSerializer(data=request.data)

        product.ProductInventory = product_serializer.data['ProductInventory'] - request.data['ProductQuantity']

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        serializer.save()
        product.save()

        return Response({
                        'status':'true',
                        'message':'Found order and added order item'
                        }, status=status.HTTP_202_ACCEPTED)


class OrderItemReadDeleteView(APIView, StaffPermission):
    permission_classes = [StaffPermission]

    def get(self, request, orderId, productId, format=None):
        orderId = int(orderId)
        productId = int(productId)
        order_view_for_id = OrderViewForId()
        order = order_view_for_id.get_order(orderId)
        if order is None:
            return order_view_for_id.NOT_FOUND_RESP

        try:
            order_item = OrderItem.objects.get(OrderId=orderId, ProductId=productId)
            serializer = OrderItemSerializer(order_item)
            return Response(serializer.data)
        except OrderItem.DoesNotExist:
            return Response({
                        'status':'false',
                        'message':'Product not found with id '+str(productId)
                        }, status=status.HTTP_404_NOT_FOUND)


    def delete(self, request, orderId, productId, format=None):
        orderId = int(orderId)
        productId = int(productId)
        order_view_for_id = OrderViewForId()
        order = order_view_for_id.get_order(orderId)
        if order is None:
            return order_view_for_id.NOT_FOUND_RESP

        order_item = None
        try:
            order_item = OrderItem.objects.get(OrderId=orderId, ProductId=productId)
        except OrderItem.DoesNotExist:
            return Response({
                        'status':'false',
                        'message':'Product not found with id '+str(productId)
                        }, status=status.HTTP_404_NOT_FOUND)

        product = Product.objects.get(ProductId=productId)
        product.ProductInventory += order_item.ProductQuantity
        product.save()
        order_item.delete()

        return Response({
                        'status':'true',
                        'message':'Found and deleted order item'
                        }, status=status.HTTP_204_NO_CONTENT)


class OrderViewForUserId(APIView, ObjectLevelOrderGetPermission):
    """
        Inhereits APIView class to encapsulate Read(GET) operation on the model/table Order
    """
    authentication_classes = (TokenAuthentication,)
    permission_classes = [ObjectLevelOrderGetPermission]

    def get_orders(self, id):
        """
            Fetch orders based on its foreign key ie orderCustomerId from the Order table
            If no id is found return None
            :param id: UserId of the orders which need to be fetched
            :return: Query set of order instance for a given user id.
                        If not found returns None
        """
        try:
            return Order.objects.filter(OrderCustomerId=int(id))
        except Order.DoesNotExist:
            self.NOT_FOUND_RESP = Response(
                {
                    "status": "false",
                    "message": "Couldn't find user " + str(id)
                },
                status=status.HTTP_404_NOT_FOUND)
            return None

    def get(self, request, id, format=None):
        """
            Fetch an instance based on its primary key ie orderId from the Order table.
            If no id is found return JSONResponse with Order Not Found message.
            :param id: Id of the instance which needs to be fetched
            :return: Order instance with given id.
                    If not found returns JSONResponse
        """
        orders = self.get_orders(id)
        if orders is None:
            return self.NOT_FOUND_RESP
        serializer = OrderSerializer(orders, many=True)
        return Response(serializer.data)