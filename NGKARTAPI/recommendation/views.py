from rest_framework.response import Response
from rest_framework.views import APIView
from product.models import Product
from permission.views import *
from recommendation.recommendation import *


class RecommendProductView(APIView):
    def get(self, request, id, format=None):
        """
            Fetch recommended products based on provided word
            :param id: Id of the instance which needs to be fetched
            :return: recommended products for given word.
        """
        product_tags_set = set(show_recommendations(id))
        products = Product.objects.all()
        filtered_product_ids = []

        for product in products:
            product_words_set = set(product.ProductName.split(' '))
            matched_words = list(product_tags_set.intersection(product_words_set))
            filtered_product_ids.append((product.ProductId, len(matched_words)))

        if len(filtered_product_ids) == 0:
            return self.NOT_FOUND_RESP

        filtered_product_ids.sort(key=lambda a: a[1])
        product_ids = [x[0] for x in filtered_product_ids]
        return Response({"products": product_ids})