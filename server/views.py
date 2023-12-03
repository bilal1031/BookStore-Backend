from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from django.db import connection
from django.shortcuts import get_object_or_404
from rest_framework.authtoken.models import Token

from django.db.models import F, IntegerField
from django.db.models.functions import Cast
from django.db.models import CharField
from django.db.models import OuterRef, Subquery

from django.contrib.auth.models import User
from store.models import Category, Book, Cart, CartItem, Order, OrderItem
from .serializers import UserSerializer, CategorySerializer, BookSerializer, CartSerializer, CartItemSerializer, OrderSerializer, OrderItemSerializer

@api_view(['POST'])
def signup(request):
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()

        # Need to use Abstract user here to add a role author or not-author for CRUD previlages for book table
        user = User.objects.get(username=request.data['username'])
        user.set_password(request.data['password'])
        user.save()
        token = Token.objects.create(user=user)
        return Response({'token': token.key, 'user': serializer.data})
    return Response(serializer.errors, status=status.HTTP_200_OK)

@api_view(['POST'])
def login(request):
    user = get_object_or_404(User, username=request.data['username'])
    if not user.check_password(request.data['password']):
        return Response("missing user", status=status.HTTP_404_NOT_FOUND)
    token, created = Token.objects.get_or_create(user=user)
    serializer = UserSerializer(user)
    return Response({'token': token.key, 'user': serializer.data})

@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def test_token(request):
    return Response("passed!")







# ------------------------------  Category API ------------------------------ 
@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def create_category(request):
    serializer = CategorySerializer(data=request.data)
    if serializer.is_valid():
        category =  serializer.save()  
        return Response({'id': category.id, 'name':request.data['name']})
    return Response(serializer.errors, status=status.HTTP_200_OK)


@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def list_categories(request):
    categories = Category.objects.all().values()
    return Response({'data': categories})



@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def get_category(request, id):
    try:
        category = Category.objects.filter(id=id).values()
        return Response({'data': category})
    except Category.DoesNotExist:
        return Response({ 'error': "category does not exsist" })


@api_view(['PUT'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def update_category(request, id):
    try:
        category = Category.objects.get(id=id)
        category.name = request.data['name']
        category.save()
        return Response({'data': {
            'id': id,
            'name': request.data['name']
        } })
    except Category.DoesNotExist:
        return Response({ 'error': "category does not exsist" })

@api_view(['DELETE'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def delete_category(request, id):
    try:
        category = Category.objects.get(id= id)
        category.delete()
        return Response({ 'deleted': 'true' })

    except Category.DoesNotExist:
        return Response({ 'deleted': 'true' })



# ------------------------------ Book API ------------------------------ 
@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def create_book(request):
    data = {
        **request.data,
        "author": request.data['author_id'],
        "category": request.data['category_id']
    }

    serializer = BookSerializer(data=data)
    if serializer.is_valid():
        book =  serializer.save()  
        return Response({'id': book.id, **request.data})
    return Response(serializer.errors, status=status.HTTP_200_OK)


@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def list_books(request):
    books = Book.objects.all().values()
    return Response({'data': books})



@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def get_book(request, id):
    try:
        book = Book.objects.filter(id=id).values()
        return Response({'data': book})
    except Book.DoesNotExist:
        return Response({ 'error': "book does not exsist" })


@api_view(['PUT'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def update_book(request, id):
    try:
        book = Book.objects.get(id=id)
        book.title = request.data['title']
        book.author = User.objects.get(pk=request.data['author_id'])
        book.category = Category.objects.get(pk=request.data['category_id'])
        book.price = request.data['price']
        book.qty = request.data['qty']

        book.save()
        return Response({'data': {
            'id': id,
            **request.data
        } })
    except book.DoesNotExist:
        return Response({ 'error': "book does not exsist" })

@api_view(['DELETE'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def delete_book(request, id):
    try:
        book = Book.objects.get(id= id)
        book.delete()
        return Response({ 'deleted': 'true' })
    except Book.DoesNotExist:
        return Response({ 'deleted': 'true' })




# ------------------------------ CART API ------------------------------ 
@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def create_cart(request):
    
    user_id = str(Token.objects.get(key = request.auth.key).user_id)

    # cart = Cart.objects.get(user_id=user_id)    
    # getting this error on using above method operator does not exist: character varying = integer
    # LINE 1: ...d" FROM "store_cart" WHERE "store_cart"."user_id" = 1 LIMIT ..

    cursor = connection.cursor()
    cursor.execute("""
    SELECT id, user_id
    FROM store_cart
    WHERE user_id = %s
    """, [user_id])

    cart = cursor.fetchall()
    cart = [{'id': id, 'user_id': user_id} for id, user_id in cart]

    if(len(cart) > 0):
        cart = cart[0]  
        data = {'qty': request.data['qty'], 'cart': cart['id'], 'book': request.data['book_id'] }
        cart_item_serializer = CartItemSerializer(data=data)
    
        print(data)
        if cart_item_serializer.is_valid():
            cart_item =  cart_item_serializer.save()
            return Response({'id': cart_item.id, **request.data})  
        else:
            return Response(cart_item_serializer.errors, status=status.HTTP_200_OK)
    else:
        return Response({'id': 'test'})  
        data = {'user_id': user_id}
        cart = CartSerializer(data=data)

        if cart.is_valid():
            cart = cart.save()
            data = {**request.data, 'cart_id': cart.id}
            cart_item_serializer = CartItemSerializer(data=data)
            if cart_item_serializer.is_valid():
                cart_item =  cart_item_serializer.save() 
                return Response({'id': cart_item.id, **request.data}) 
            else:
                return Response(cart_item_serializer.errors, status=status.HTTP_200_OK)


@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def get_cart(request, id):
    try:


        # is_there_cart = Cart.objects.filter(user_id= id).exists()   
        # getting this error on using above method operator does not exist: character varying = integer
        # LINE 1: ...d" FROM "store_cart" WHERE "store_cart"."user_id" = 1 LIMIT ..

        cursor = connection.cursor()
        cursor.execute("""
        SELECT id, user_id
        FROM store_cart
        WHERE user_id = %s
        """, [str(id)])

        cart = cursor.fetchall()
        cart = [{'id': id, 'user_id': user_id} for id, user_id in cart]

        if(len(cart) > 0):
            cart = cart[0] 
        
            # cart_items = CartItem.objects.filter(cart_id= "%s" % (cart['id']))
            
            cursor = connection.cursor()
            cursor.execute("""
            SELECT "store_cartitem"."id", "store_cartitem"."cart_id", "store_cartitem"."book_id", "store_cartitem"."qty" FROM "store_cartitem" WHERE "store_cartitem"."cart_id" = %s
            """, [str(cart['id'])])

            cart_items = cursor.fetchall()
            cart_items = [{'id':id, 'cart_id': cart, 'book_id': book, 'qty': qty} for id, cart, book, qty in cart_items]
            print(cart_items)
            return Response({ 
                'data': {
                        'cart_id': cart['id'],
                        'items': cart_items
                        } 
            })
        else:
            return Response({ 'data': [] })

    except Cart.DoesNotExist:
        return Response({ 'error': "Cart does not exsist" })


@api_view(['PATCH'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def update_cart(request, id):
    try:

        cart_item = CartItem.objects.get(id=id)
        cart_item.qty = request.data['qty']
        cart_item.save()
        
        return Response({'data': {
            'id': id,
            **request.data
        } })
    except CartItem.DoesNotExist:
        return Response({ 'error': "Cart Item does not exsist" })


@api_view(['DELETE'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def delete_cart(request, id):
    try:
        cart_item = CartItem.objects.get(id= id)
        cart_item.delete()

        user_id = Token.objects.get(key=request.auth.key).user_id
        cart = Cart.objects.filter(user_id= user_id).first()

        cart_items = CartItem.objects.filter(cart_id= cart.id).values()
        return Response({ 
            'data': {
                    'cart_id': cart.id,
                    'items': cart_items
                    } 
        })

    except CartItem.DoesNotExist:
        return Response({ 'error': "Cart Item does not exsist" })


# ------------------------------ ORDER API ------------------------------ 

@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def create_order(request):
    try:
        # Left join cart and book items for get price of book from book table
        #  Issue here: Below code giving same issue as above 
        # operator does not exist: character varying = integer
        # LINE 1: ..." FROM "store_cartitem" WHERE "store_cartitem"."cart_id" = 2
        # The request.data['cart_id'] is type casted but still the query process it as integer
        cart_items_with_price = CartItem.objects.filter(cart_id= str(request.data['cart_id'])) \
            .select_related('book')
            #  \
            # .annotate(
            #     price=Subquery(
            #         Book.objects.filter(pk=OuterRef('book'))
            #         .values('price')[:1]
            #     )
            # )
        return Response({ 'data':  cart_items_with_price.values() })

        if cart_items.exists():
            user_id = Token.objects.get(key=request.auth.key).user_id

            total_order_price = sum(item.book.price for item in cart_items)

            data = {'user_id': user_id, 'status': "active", 'price': total_order_price}
            order_serializer = OrderSerializer(data=data)

            if order_serializer.is_valid():
                order = order_serializer.save()

                for item in cart_items:    
                    data = { 'order_id': order.id , 'book_id': item.book_id, 'qty': item.qty}
                    order_item_serializer = OrderItemSerializer(data=data)
                    if order_item_serializer.is_valid():
                        order_item = order_item_serializer.save()
                        item.delete()

                return Response({ 'data': {
                    order_id: order.id,
                    items: cart_items.values()
                } })

        else:
            return Response({ 'error': "Cart is empty!" })

    except CartItem.DoesNotExist:
        return Response({ 'error': "Cart does not exsist" })



@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def get_order(request, id):
    try:
        
        return Response({ 'data': Order.objects.all().values() })

        is_there_order = Order.objects.filter(user_id= id)
        if(is_there_order.exists()):
            order = is_there_order.first()
            order_items = OrderItem.objects.filter(order_id= order.id).values()
            return Response({ 
                'data': {
                            'order_id': order.id,
                            'price': order.price,
                            'items': order_itemss
                        } 
            })
        else:
            return Response({ 'data': [] })

    except Order.DoesNotExist:
        return Response({ 'error': "Order does not exsist" })


# @api_view(['PATCH'])
# @authentication_classes([TokenAuthentication])
# @permission_classes([IsAuthenticated])
# def update_order(request, id):
#     try:

#         order_item = CartItem.objects.get(id=id)
#         order_item.qty = request.data['qty']

#         return Response({'data': {
#             'id': id,
#             **request.data
#         } })
#     except CartItem.DoesNotExist:
#         return Response({ 'error': "Cart Item does not exsist" })


# @api_view(['DELETE'])
# @authentication_classes([TokenAuthentication])
# @permission_classes([IsAuthenticated])
# def delete_order(request, id):
#     try:
#         order_item = CartItem.objects.get(id= id)
#         order_item.delete()

#         user_id = Token.objects.get(key=request.auth.key).user_id
#         order = Cart.objects.filter(user_id= user_id).first()

#         order_items = CartItem.objects.filter(order_id= order.id).values()
#         return Response({ 
#             'data': {
#                     'order_id': order.id,
#                     'items': order_items
#                     } 
#         })

#     except CartItem.DoesNotExist:
#         return Response({ 'error': "Cart Item does not exsist" })