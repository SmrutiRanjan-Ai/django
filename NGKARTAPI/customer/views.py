from django.shortcuts import render
from django.http import Http404
from django.http.response import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.files.storage import default_storage
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.parsers import JSONParser
from rest_framework import status
from rest_framework.views import APIView
from customer.models import *
from customer.serializers import *
from permission.views import DefaultWritePermission
from rest_framework.authentication import TokenAuthentication
from rest_framework import permissions
# Create your views here.

class ShippingAddressViewList(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (permissions.AllowAny,)
    """
        Inhereits APIView class to encapsulate Read(GET) and Create(POST) operations on
        the model/table ShippingAddress
    """
    def get(self, request, format=None):
        """
            Returns all instances of the table ShippingAddress

            :param request: Request object
            :param format: Format of the input. Default is JSON
            :return: Response object with serialized data corrsponding to all shipping address instances 
        """
        shipping_addrs = ShippingAddress.objects.all()
        serializer = ShippingAddressSerializer(shipping_addrs, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        """
            Saves the data accompanied by the request as an new instance
            in the ShippingAddress table if its valid.

            :param request: Request object
            :param format: Format of the input. Default is JSON
            :return: Response object with serialized data corrsponding to added shippingaddress instance 
        """
        serializer = ShippingAddressSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ShippingAddressViewForID(APIView):

    """
        Inhereits APIView class to encapsulate Read(GET), Update(PUT) and Delete(DELETE) 
        operations on the model/table ShippingAddress given a specific ShippingAddressId (unique).
    """
    def get_object(self, id):
        """
            Fetch an instance based on its primary key ie ShippingAddressId.
            If no instance for the id is found return None

            :param id: Id of the instance which needs to be fetched
            :return: ShippingAddress instance with given id. 
                    If not found returns None
        """
        try:
            shipping_addr = ShippingAddress.objects.get(ShippingAddressId=id)
            return shipping_addr
        except ShippingAddress.DoesNotExist:
            self.NOT_FOUND_RESP = Response({id : "Shipping Address Not Found"}, status=status.HTTP_404_NOT_FOUND)
            return None

    def get(self, request, id, format=None):
        """
            Fetch an instance based on its primary key ie ShippingAddressId.
            If no instance is found return JSONResponse with ShippingAddress Not Found message.

            :param id: Id of the instance which needs to be fetched
            :return: ShippingAddress instance with given id. 
                    If not found returns JSONResponse
        """
        shipping_addr = self.get_object(id)
        if shipping_addr is None:
            return self.NOT_FOUND_RESP
        serializer = ShippingAddressSerializer(shipping_addr)
        return Response(serializer.data)
    
    def put(self, request, id, format=None):
        """
            Fetch an instance based on its primary key ie ShippingAddressId.
            Update that instance with the data accompanied with the request.
            If no such instance is found return JSONResponse with ShippingAddress Not Found message.

            :param id: Id of the instance which needs to be updated
            :return: Update ShippingAddress instance with given id. 
                        If not found returns JSONResponse
        """
        shipping_addr = self.get_object(id)
        if shipping_addr is None:
            return self.NOT_FOUND_RESP
        serializer = ShippingAddressSerializer(shipping_addr, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)
    
    def delete(self, request, id, format=None):
        """
            Fetch an instance based on its primary key ie ShippingAddressId. Delete the instance.
            If no such instance is found return JSONResponse with ShippingAddress Not Found message.

            :param id: Id of the instance which needs to be deleted
            :return: Delete ShippingAddress instance with given id. Returns HTTP 204 response
                        If not found returns JSONResponse
        """
        shipping_addr = self.get_object(id)
        if shipping_addr is None:
            return self.NOT_FOUND_RESP
        shipping_addr.delete()
        return Response(status=HTTTP_204_BAD_NO_CONTENT)


class ShippingAddressViewForCustomerId(APIView):
    """
        Inhereits APIView class to encapsulate Read(GET) and Delete(DELETE) operations 
        on the model/table ShippingAddress for a given CustomerId.
    """

    def get_objects(self, id):
        """
            Fetch instances from ShippingAddress table based on its foreign key ie CustomerId
            If no instance for the id is found return None

            :param id: Id of the instance which needs to be fetched
            :return: ShippingAddress instance with given id. 
                    If not found returns None
        """
        try:
            return ShippingAddress.objects.filter(ShippingAddressCustomerId=id)
        except ShippingAddress.DoesNotExist:
            self.NOT_FOUND_RESP = Response({id : "Shipping Address(s) Not Found"}, status=status.HTTP_404_NOT_FOUND)
            return None

    def get(self, request, id, format=None):
        """
            Returns all instances of the table ShippingAddress

            :param request: Request object
            :param id: Customer Id
            :param format: Format of the input. Default is JSON
            :return: Response object with serialized data corrsponding to all shippingaddress instances 
        """
        shipping_addrs = self.get_objects(id)
        if shipping_addrs is None:
            return self.NOT_FOUND_RESP
        serializer = ShippingAddressSerializer(shipping_addrs, many=True)
        return Response(serializer.data)

    def delete(self, request, id, format=None):
        """
            Deletes the instances from ShippingAddress table for a specific CustomerId.

            :param request: Request object
            :param id: Customer Id
            :param format: Format of the input. Default is JSON
            :return: Delete ShippingAddress instance with given CustomerId.
                    Returns HTTP 204 response. If not found returns JSONResponse
        """
        shipping_addrs = self.get_objects(id)
        if shipping_addrs is None:
            return self.NOT_FOUND_RESP
        for addr in shipping_addrs:
            addr.delete()
        return Response(status=HTTTP_204_BAD_NO_CONTENT)
