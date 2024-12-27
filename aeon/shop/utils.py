import redis
from .models import ProductProxy
from django.db.models import Case, When
import dotenv
import os

#redis client
r = redis.Redis(
    host=os.getenv('REDIS_HOST'), 
    port=int(os.getenv('REDIS_PORT')), 
    decode_responses=True)

def get_user_id_for_redis(request):
    if not request.session.session_key:
        request.session.save()
    return str(request.session.session_key) if request.user.is_anonymous else str(request.user.id)

def create_product_history_by_user(user_id, product_id):
    product_history_length = r.lpush(user_id, product_id)
    r.expire(user_id, 60*60*24*30)
    print(f"Updated list for {user_id}: {r.lrange(user_id, 0, -1)}")
    return product_history_length

def get_products_ids_by_user(user_id):
    last_viewed_products_ids = r.lrange(user_id, 0, -1)
    last_viewed_products_ids_list = [int(id) for id in last_viewed_products_ids]
    return last_viewed_products_ids_list

def get_product_history_queryset_by_user(product_ids, product_id):
    last_viewed_products_queryset = ProductProxy.objects.filter(
        id__in=product_ids
    ).exclude(id=product_id)

    preserved_order = Case(*[When(id=pk, then=pos) for pos, pk in enumerate(product_ids)])
    last_viewed_products_queryset = last_viewed_products_queryset.order_by(preserved_order)
    
    print(last_viewed_products_queryset)
    return last_viewed_products_queryset

def limit_product_history_length(user_id, product_history_length):
    if product_history_length > 5:
        r.rpop(user_id)

def replace_visited_product(user_id, product_id):
    r.lrem(user_id, 0, product_id)
    create_product_history_by_user(user_id, product_id)