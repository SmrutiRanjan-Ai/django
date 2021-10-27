from rest_framework.response import Response
from rest_framework import status,permissions
from rest_framework.views import APIView
from site_meta.models import *
from site_meta.serializers import *
from permission.views import DefaultWritePermission


# Create your views here.
class SiteMetadataViewForTitle(APIView, DefaultWritePermission):
    """
        Inhereits APIView class to encapsulate Read(GET)
        operations on the model/table SiteMetaData given a specific SiteTitle.
    """
    permission_classes = [DefaultWritePermission]

    def get_objects(self, id):
        """
            Fetch instances based on SiteTitle from the SiteMetaData table
            If no such instance is found return None
            :param id: Title of the instances which need to be fetched
            :return: SiteMetaData instance with given title.
                        If not found returns None
        """
        try:
            return SiteMetaData.objects.filter(SiteTitle=id)
        except SiteMetaData.DoesNotExist:
            self.NOT_FOUND_RESP = Response({id: "SiteMetaData Not Found"}, status=status.HTTP_404_NOT_FOUND)
            return None

    def get(self, request, id, format=None):
        """
            Fetch instances based on title from the SiteMetaData table.
            If no such instance is found return JSONResponse with SiteMetaData Not Found message.
            :param id: Title of the instances which need to be fetched
            :return: SiteMetData instances with given title.
                    If not found returns JSONResponse
        """
        sites = self.get_objects(id)
        if sites is None:
            return self.NOT_FOUND_RESP
        serializer = SiteMetaDataSerializer(sites, many=True)
        return Response(serializer.data)


class SiteMetaDataViewList(APIView, DefaultWritePermission):
    """
        Inhereits APIView class to encapsulate Read(GET) and Create(POST) operations on
        the model/table SiteMetaData
    """
    permission_classes = [DefaultWritePermission]

    def get(self, request, format=None):
        """
            Returns all instances of the table SiteMetaData
            :param request: Request object
            :param format: Format of the input. Default is JSON
            :return: Response object with serialized data corrsponding to all SiteMetaData instances
        """
        sites = SiteMetaData.objects.all()
        serializer = SiteMetaDataSerializer(sites, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        """
            Saves the data accompanied by the request as an new instance
            in the SiteMetaData table if its valid.
            :param request: Request object
            :param format: Format of the input. Default is JSON
            :return: Response object with serialized data corrsponding to added SiteMetaData instance
        """
        serializer = SiteMetaDataSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SiteMetadataViewForId(APIView, DefaultWritePermission):
    """
        Inhereits APIView class to encapsulate Read(GET), Update(PUT) and Delete(DELETE)
        operations on the model/table SiteMetaData given a specific SiteId (unique).
    """
    permission_classes = [DefaultWritePermission]

    def get_object(self, id):
        """
            Fetch an instance based on its primary key ie SiteId from the SiteMetaData table
            If no id is found return None
            :param id: Id of the instance which needs to be fetched
            :return: SiteMetaData instance with given id.
                        If not found returns None
        """
        try:
            return SiteMetaData.objects.get(SiteId=id)
        except SiteMetaData.DoesNotExist:
            self.NOT_FOUND_RESP = Response({id: "SiteMetaData Not Found"}, status=status.HTTP_404_NOT_FOUND)
            return None

    def get(self, request, id, format=None):
        """
            Fetch an instance based on its primary key ie id from the SiteMetaData table.
            If no id is found return JSONResponse with SiteMetaData Not Found message.
            :param id: Id of the instance which needs to be fetched
            :return: SiteMetData instance with given id.
                    If not found returns JSONResponse
        """
        site = self.get_object(id)
        if site is None:
            return self.NOT_FOUND_RESP
        serializer = SiteMetaDataSerializer(site)
        return Response(serializer.data)

    def put(self, request, id, format=None):
        """
            Fetch an instance based on its primary key ie id from SiteMetaData table
            Update that instance with the data accompanied with the request.
            If no such instance is found return JSONResponse with SiteMetaData Not Found message.
            :param id: Id of the instance which needs to be updated
            :return: Update SiteMetaData instance with given id.
                        If not found returns JSONResponse
        """
        site = self.get_object(id)
        if site is None:
            return self.NOT_FOUND_RESP
        serializer = SiteMetaDataSerializer(site, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


def delete(self, request, id, format=None):
    """
        Fetch an instance from SiteMetaData table based on its primary key ie id. Delete the instance.
        If no such instance is found return JSONResponse with SiteMetaData Not Found message.
        :param id: Id of the instance which needs to be deleted
        :return: Delete SiteMetadata instance with given id. Returns HTTP 204 response
                    If not found returns JSONResponse
    """
    site = self.get_object(id)
    if site is None:
        return self.NOT_FOUND_RESP
    site.delete()
    return Response(status=status.HTTTP_204_BAD_NO_CONTENT)


class FileUploadViewList(APIView):
    permission_classes = (permissions.AllowAny,)
    """
        Inhereits APIView class to encapsulate Read(GET) and Create(POST) operations on
        the model/table FileUpload
    """

    def get(self, request, format=None):
        """
            Returns all instances of the table FileUpload
            :param request: Request object
            :param format: Format of the input. Default is JSON
            :return: Response object with serialized data corrsponding to all FileUpload instances
        """
        files = FileUpload.objects.all()
        serializer = FileUploadSerializer(files, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        """
            Saves the data accompanied by the request as an new instance
            in the FileUpload table if its valid.
            :param request: Request object
            :param format: Format of the input. Default is JSON
            :return: Response object with serialized data corrsponding to added FileUpload instance
        """
        serializer = FileUploadSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class FileUploadViewForId(APIView):
    """
        Inhereits APIView class to encapsulate Read(GET), Update(PUT) and Delete(DELETE)
        operations on the model/table FileUpload given a specific FileId (unique).
    """

    def get_object(self, id):
        """
            Fetch an instance based on its primary key ie FileId from the FileUpload table
            If no id is found return None
            :param id: Id of the instance which needs to be fetched
            :return: FileUpload instance with given FileId.
                        If not found returns None
        """
        try:
            return FileUpload.objects.get(FileId=id)
        except FileUpload.DoesNotExist:
            self.NOT_FOUND_RESP = Response({id: "File Not Found"}, status=status.HTTP_404_NOT_FOUND)
            return None

    def get(self, request, id, format=None):
        """
            Fetch an instance based on its primary key ie id from the FileUpload table.
            If no id is found return JSONResponse with File Not Found message.
            :param id: Id of the instance which needs to be fetched
            :return: FileUpload instance with given id.
                    If not found returns JSONResponse
        """
        file = self.get_object(id)
        if file is None:
            return self.NOT_FOUND_RESP
        serializer = FileUploadSerializer(file)
        return Response(serializer.data)

    def put(self, request, id, format=None):
        """
            Fetch an instance based on its primary key ie id from FileUpload table
            Update that instance with the data accompanied with the request.
            If no such instance is found return JSONResponse with File Not Found message.
            :param id: Id of the instance which needs to be updated
            :return: Update FileUpload instance with given id.
                        If not found returns JSONResponse
        """
        file = self.get_object(id)
        if file is None:
            return self.NOT_FOUND_RESP
        serializer = FileUploadSerializer(file, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id, format=None):
        """
            Fetch an instance from FileUpload table based on its primary key ie id. Delete the instance.
            If no such instance is found return JSONResponse with FileUpload Not Found message.
            :param id: Id of the instance which needs to be deleted
            :return: Delete FileUpload instance with given id. Returns HTTP 204 response
                        If not found returns JSONResponse
        """
        file = self.get_object(id)
        if file is None:
            return self.NOT_FOUND_RESP
        file.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)