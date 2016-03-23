from decimal import Decimal
from django.conf import settings
from shop.models import Product

class Cart(object):

	def __init__(self, request):
		"""
		카트 초기화
		세션에 대해서 다음 페이지 참조:
		https://docs.djangoproject.com/en/1.9/topics/http/sessions/
		"""
		self.session = request.session
		cart = self.session.get(settings.CART_SESSION_ID)
		if not cart:
			# 세션에 비어있는 카트를 저장한다.
			cart = self.session[settings.CART_SESSION_ID] = {}
		self.cart = cart

	def add(self,product,quantity=1,update_quantity=False):
		"""
		카트에 상품을 추가하거나 수량을 조정함
		"""
		product_id = str(product.id)
		if product_id not in self.cart:
			self.cart[product_id] = {'quantity': 0,
									'price': str(product.price)}
		if update_quantity:
			self.cart[product_id]['quantity'] = quantity
		else:
			self.cart[product_id]['quantity'] += quantity
		self.save()

	def save(self):
		# 카트 세션 업데이트
		self.session[settings.CART_SESSION_ID] = self.cart
		# 세션이 수정되었다고 장고에게 알려 세션을 새로 저장 함
		self.session.modified = True

	def remove(self, product):
		"""
		카트에서 상품을 제거함
		"""
		product_id = str(product.id)
		if product_id in self.cart:
			del self.cart[product_id]
			self.save()

	def __iter__(self):
		"""
		Iterate over the items in the cart and get the products
		from the database.
		"""
		product_ids = self.cart.keys()
		# 상품 객체를 조회하여 카트에 넣는다.
		products = Product.objects.filter(id__in=product_ids)
		for product in products:
			self.cart[str(product.id)]['product'] = product
		for item in self.cart.values():
			item['price'] = Decimal(item['price'])
			item['total_price'] = item['price'] * item['quantity']
			yield item

	def __len__(self):
		"""
		Count all items in the cart.
		"""
		return sum(item['quantity'] for item in self.cart.values())

	def get_total_price(self):
		return sum(Decimal(item['price']) * item['quantity'] for item in
		self.cart.values())

	def clear(self):
		# remove cart from session
		del self.session[settings.CART_SESSION_ID]
		self.session.modified = True
