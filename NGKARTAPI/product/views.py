from django.http import Http404
from django.http.response import HttpResponse, JsonResponse
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from product.models import *
from product.serializers import *
from permission.views import DefaultWritePermission
from rest_framework.authentication import TokenAuthentication
from rest_framework.parsers import JSONParser, FileUploadParser


class ProductViewList(APIView, DefaultWritePermission):
    """
        Inhereits APIView class to encapsulate Read(GET) and Create(POST) operations on
        the model/table Product
    """
    authentication_classes = (TokenAuthentication,)
    permission_classes = [DefaultWritePermission]
    def get(self, request, format=None):
        """
            Returns all instances of the table Product

            :param request: Request object
            :param format: Format of the input. Default is JSON
            :return: Response object with serialized data corrsponding to all product instances 
        """
        products = Product.objects.all()
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        """
            Saves the data accompanied by the request as an new instance
            in the Product table if its valid.

            :param request: Request object
            :param format: Format of the input. Default is JSON
            :return: Response object with serialized data corrsponding to added product instance 
        """
        product_data = JSONParser().parse(request)
        serializer = ProductSerializer(data=product_data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProductViewForIdAndSlug(APIView, DefaultWritePermission):
    """
        Inhereits APIView class to encapsulate Read(GET), Update(PUT) and Delete(DELETE) 
        operations on the model/table Product given a specific product id (unique).
    """
    authentication_classes = (TokenAuthentication,)
    permission_classes = [DefaultWritePermission]
    def get_object(self, id):
        """
            Fetch an instance based on its primary key ie id.
            If no id is found return None

            :param id: Id of the instance which needs to be fetched
            :return: product instance with given id. 
                    If not found returns None
        """
        try:
            try:
                return Product.objects.get(ProductId=int(id))
            except ValueError as e:
                return Product.objects.get(ProductSlug=id)
        except Product.DoesNotExist:
            self.NOT_FOUND_RESP = Response({id : "Product Not Found"}, status=status.HTTP_404_NOT_FOUND)
            return None

    def get(self, request, id, format=None):
        """
            Fetch an instance based on its primary key ie id.
            If no id is found return JSONResponse with Product Not Found message.

            :param id: Id of the instance which needs to be fetched
            :return: product instance with given id. 
                    If not found returns JSONResponse
        """
        product = self.get_object(id)
        if product is None:
            return self.NOT_FOUND_RESP
        serializer = ProductSerializer(product)
        return Response(serializer.data)
    
    def put(self, request, id, format=None):
        """
            Fetch an instance based on its primary key ie id.
            Update that instance with the data accompanied with the request.
            If no such instance is found return JSONResponse with Product Not Found message.

            :param id: Id of the instance which needs to be updated
            :return: Update product instance with given id. 
                        If not found returns JSONResponse
        """
        product = self.get_object(id)
        if product is None:
            return self.NOT_FOUND_RESP
        serializer = ProductSerializer(product, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, id, format=None):
        """
            Fetch an instance based on its primary key ie id. Delete the instance.
            If no such instance is found return JSONResponse with Product Not Found message.

            :param id: Id of the instance which needs to be deleted
            :return: Delete product instance with given id. Returns HTTP 204 response
                        If not found returns JSONResponse
        """
        product = self.get_object(id)
        if product is None:
            return self.NOT_FOUND_RESP
        product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class LatestProductList(APIView):
    """
        Inhereits APIView class to encapsulate Read(GET) operation for retrieving lastest products
        from the model/table Product.
    """
    def get(self, request, num_latest=5, format=None):
        """
            Returns latest instances of the table Product

            :param request: Request object
            :param request: Optional arg specifying no of latest products to be retrieved
            :param format: Format of the input. Default is JSON
            :return: Response object with serialized data corrsponding to all latest product instances 
        """
        all_products = Product.objects.all()
        if len(all_products)<num_latest:
            num_latest = len(all_products)
        products = all_products[:num_latest] 
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)


class ProductViewForCategory(APIView):
    """
        Inhereits APIView class to encapsulate Read(GET) operation for retrieving all products
        from a particular category specified categoryslug.
    """
    def get_object(self, category_slug):
        try:
            return Product.objects.filter(ProductCategories__CategorySlug=category_slug)
        except (Category.DoesNotExist, Product.DoesNotExist) as e:
            raise Http404
        
    def get(self, request, category_slug, format=None):
        product = self.get_object(category_slug)
        serializer = ProductSerializer(product, many=True)
        return Response(serializer.data)


class TaxViewList(APIView, DefaultWritePermission):
    """
        Inhereits APIView class to encapsulate Read(GET) and Create(POST) operations on
        the model/table Tax
    """
    permission_classes = [DefaultWritePermission]
    def get(self, request, format=None):
        """
            Returns all instances of the table Tax

            :param request: Request object
            :param format: Format of the input. Default is JSON
            :return: Response object with serialized data corrsponding to all tax instances 
        """
        taxes = Tax.objects.all()
        serializer = TaxSerializer(taxes, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        """
            Saves the data accompanied by the request as an new instance
            in the Tax table if its valid.

            :param request: Request object
            :param format: Format of the input. Default is JSON
            :return: Response object with serialized data corrsponding to added tax instance 
        """
        serializer = TaxSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TaxViewForId(APIView, DefaultWritePermission):
    """
        Inhereits APIView class to encapsulate Read(GET), Update(PUT) and Delete(DELETE) 
        operations on the model/table Tax given a specific Tax id (unique).
    """
    permission_classes = [DefaultWritePermission]
    def get_object(self, id):
        """
            Fetch an instance based on its primary key ie id from the Tax table
            If no id is found return None

            :param id: Id of the instance which needs to be fetched
            :return: Tax instance with given id. 
                        If not found returns None
        """
        try:
            return Tax.objects.get(TaxId=id)
        except Tax.DoesNotExist:
            self.NOT_FOUND_RESP = Response({"message" : "Tax Not Found"}, status=status.HTTP_404_NOT_FOUND)
            return None

    def get(self, request, id, format=None):
        """
            Fetch an instance based on its primary key ie id from the tax table.
            If no id is found return JSONResponse with Tax Not Found message.

            :param id: Id of the instance which needs to be fetched
            :return: tax instance with given id. 
                    If not found returns JSONResponse
        """
        tax = self.get_object(id)
        if tax is None:
            return self.NOT_FOUND_RESP
        serializer = TaxSerializer(tax)
        return Response(serializer.data)
    
    def put(self, request, id, format=None):
        """
            Fetch an instance based on its primary key ie id from Tax table
            Update that instance with the data accompanied with the request.
            If no such instance is found return JSONResponse with Tax Not Found message.

            :param id: Id of the instance which needs to be updated
            :return: Update tax instance with given id. 
                        If not found returns JSONResponse
        """
        tax = self.get_object(id)
        if tax is None:
            return self.NOT_FOUND_RESP
        serializer = TaxSerializer(tax, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, id, format=None):
        """
            Fetch an instance from Tax table based on its primary key ie id. Delete the instance.
            If no such instance is found return JSONResponse with Tax Not Found message.

            :param id: Id of the instance which needs to be deleted
            :return: Delete tax instance with given id. Returns HTTP 204 response
                        If not found returns JSONResponse
        """
        tax = self.get_object(id)
        if tax is None:
            return self.NOT_FOUND_RESP
        tax.delete()
        return Response(status=status.HTTTP_204_BAD_NO_CONTENT)


class TagViewList(APIView, DefaultWritePermission):
    """
        Inhereits APIView class to encapsulate Read(GET) and Create(POST) operations on
        the model/table Tag
    """
    permission_classes = [DefaultWritePermission]
    def get(self, request, format=None):
        """
            Returns all instances of the table Tag

            :param request: Request object
            :param format: Format of the input. Default is JSON
            :return: Response object with serialized data corrsponding to all tag instances 
        """
        tags = Tag.objects.all()
        serializer = TagSerializer(tags, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        """
            Saves the data accompanied by the request as an new instance
            in the Tag table if its valid.

            :param request: Request object
            :param format: Format of the input. Default is JSON
            :return: Response object with serialized data corrsponding to added tag instance 
        """
        serializer = TagSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TagViewForSlug(APIView, DefaultWritePermission):
    """
        Inhereits APIView class to encapsulate Read(GET), Update(PUT) and Delete(DELETE) 
        operations on the model/table Tag given a specific tag id(unique) or tag name (unique).
    """
    permission_classes = [DefaultWritePermission]
    def get_object(self, slug):
        """
            Fetch an instance based on its primary key ie slug from the Tag table
            If not found return None

            :param id: slug of the instance which needs to be fetched
            :return: Tag instance with given tag_slug. 
                        If not found returns None
        """
        tag_slug = slug.capitalize()
        try:
            tag = Tag.objects.get(TagSlug=tag_slug)
        except:
            self.NOT_FOUND_RESP = Response({tag_slug : "Tag Not Found"}, status=status.HTTP_404_NOT_FOUND)
            return None
        return tag

    def get(self, request, slug, format=None):
        """
            Fetch an instance based on its primary key ie tag_slug from the tag table.
            If no such instance is found return JSONResponse with Tag Not Found message.

            :param id: slug of the instance which needs to be fetched
            :return: Tag instance with given slug. 
                    If not found returns JSONResponse
        """
        tag = self.get_object(slug)
        if tag is None:
            return self.NOT_FOUND_RESP
        serializer = TagSerializer(tag)
        return Response(serializer.data)
    
    def put(self, request, slug, format=None):
        """
            Fetch an instance based on its primary key ie tag_slug from the tag table.
            If no such instance is found return JSONResponse with Tag Not Found message.
            If found update that instance with the data accompanied with the request.

            :param id: slug of the instance which needs to be updated
            :return: Update tag instance with given slug. 
                        If not found returns JSONResponse
        """
        tag = self.get_object(slug)
        if tag is None:
            return self.NOT_FOUND_RESP
        serializer = TagSerializer(tag, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, slug, format=None):
        """
            Fetch an instance from Tag table based on its primary key tag_slug
            If no such instance is found return JSONResponse with Tag Not Found message.
            If found delete that instance.

            :param id: Slug of the instance which needs to be deleted
            :return: Delete tag instance with given slug. Returns HTTP 204 response
                        If not found returns JSONResponse
        """
        tag = self.get_object(slug)
        if tag is None:
            return self.NOT_FOUND_RESP
        tag.delete()
        return Response(status=status.HTTTP_204_BAD_NO_CONTENT)


class CategoryViewList(APIView, DefaultWritePermission):
    """
        Inhereits APIView class to encapsulate Read(GET) and Create(POST) operations on
        the model/table Category
    """
    authentication_classes = (TokenAuthentication,)
    permission_classes = [DefaultWritePermission]
    parser_class = (FileUploadParser,)
    def get(self, request, format=None):
        """
            Returns all instances of the table Category

            :param request: Request object
            :param format: Format of the input. Default is JSON
            :return: Response object with serialized data corrsponding to all Category instances 
        """
        categories = Category.objects.all()
        serializer = CategorySerializer(categories, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        """
            Saves the data accompanied by the request as an new instance
            in the Category table if its valid.

            :param request: Request object
            :param format: Format of the input. Default is JSON
            :return: Response object with serialized data corrsponding to added Category instance 
        """
        serializer = CategorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CategoryViewForSlug(APIView, DefaultWritePermission):
    """
        Inhereits APIView class to encapsulate Read(GET), Update(PUT) and Delete(DELETE) 
        operations on the model/table Category given a specific Category id(unique) or Category name (unique).
    """
    permission_classes = [DefaultWritePermission]
    def get_object(self, slug):
        """
            Fetch an instance based on its primary key ie id from the Category table
            If no instance with the id is found, consider the same id as Category name 
            to fetch an instance. If not found return None

            :param id: Id or name of the instance which needs to be fetched
            :return: Category instance with given category_id or category_name. 
                        If not found returns None
        """
        category_slug = slug.capitalize()
        try:
            category = Category.objects.get(CategorySlug=category_slug)
        except Category.DoesNotExist:
            self.NOT_FOUND_RESP = Response({category_slug : "Category Not Found"}, status=status.HTTP_404_NOT_FOUND)
            return None
        return category

    def get(self, request, slug, format=None):
        """
            Fetch an instance based on its primary key ie tag_id from the tag table.
            If no instance with that tag_id is found, fetch an instance with the id as tag_name
            If no such instance is found return JSONResponse with Tag Not Found message.
            If found update that instance with the data accompanied with the request.

            :param id: Id of the instance which needs to be updated
            :return: Update tax instance with given id. 
                        If not found returns JSONResponse
        """
        category = self.get_object(slug)
        if category is None:
            return self.NOT_FOUND_RESP 
        serializer = CategorySerializer(category)
        return Response(serializer.data)
    
    def put(self, request, slug, format=None):
        """
            Fetch an instance based on its primary key ie category_id from the category table.
            If no instance with that category_id is found, fetch an instance with the id as category_name
            If no such instance is found return JSONResponse with Category Not Found message.
            If found update that instance with the data accompanied with the request.

            :param id: Id of the instance which needs to be updated
            :return: Update Category instance with given id.
                        If not found returns JSONResponse
        """
        category = self.get_object(slug)
        if category is None:
            return self.NOT_FOUND_RESP
        serializer = CategorySerializer(category, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, slug, format=None):
        """
            Fetch an instance from Category table based on its primary key category_id
            If no instance with that category_id is found, fetch an instance with the id as category_name
            If no such instance is found return JSONResponse with Category Not Found message.
            If found delete that instance.

            :param id: Id of the instance which needs to be deleted
            :return: Delete Category instance with given id. Returns HTTP 204 response
                        If not found returns JSONResponse
        """
        category = self.get_object(slug)
        if category is None:
            return self.NOT_FOUND_RESP
        category.delete()
        return Response(status=status.HTTTP_204_BAD_NO_CONTENT)

