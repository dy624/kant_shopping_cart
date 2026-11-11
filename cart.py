from product import Product
from coupon import  PercentCoupon, FixedCoupon

class Cart:
    def __init__(self):
        # 빈 장바구니 생성
        self.items = {} # {상품 : 수량}
        self.coupon = None


    # 장바구니에 상품 담기
    def add(self, product, qty): 
        # 품절 상품은 담을 수 없다.
        if product.is_sold_out():
            print("품절된 상품입니다.") 
            return 

        # 이미 장바구니에 담겨있는 수량
        in_cart_qty = self.items.get(product, 0)
      
        # 더 담을 수 있는 수량
        extra_qty = product.stock - in_cart_qty
        if qty > extra_qty: # 재고 수량 범위를 벗어난 경우
            print(f"재고가 부족합니다. (담을 수 있는 수량:{extra_qty}개)")
            return

        self.items[product] = self.items.get(product, 0) + qty
        print(f"{product.name} {qty}개를 담았습니다.")


    # 장바구니에서 상품 제거(빼기)
    def remove(self, product, qty):
        # 장바구니에 없는 상품은 뺄수 없다.
        if product not in self.items:
            print("장바구니에 해당 상품이 없습니다.")
            return

        # 담은 수량 이상 빼면 삳품을 통째로 삭제
        if qty >= self.items[product]:
            del self.items[product]  # 해당 상품을 딕셔너리에서 삭제
            print(f"{product.name}를 장바구니에서 모두 뺐습니다.")

        else:
            self.items[product] -= qty
            print(f"{product.name} {qty}개를 뺐습니다.") 


    # 장바구니 비었는지 확인
    def is_empty(self):
        return len(self.items) == 0

    # 상품 합계 계산
    def subtotal(self):
        return sum(p.price * q for p,q in self.items.items())

    # 배송비
    def shipping(self):
        if self.is_empty(): return 0
        return 0 if self.subtotal() >= 30_000 else 3_000


    # 결제 금액 계산
    def total(self):
        return self.subtotal() - self.discount() + self.shipping()

    # 장바구니 내용 출력
    def show(self):
        line = "-" * 40
        print(line)

        if self.is_empty():
            print("장바구니 비어있습니다.")

        for p, q in self.items.items():
            # 제품명 x 수량
            print(f"{p.name:<10} x {q:<3} = {p.price * q:>12,}원")

        print(line)
        print(f"{'상품 합계':<10} {self.subtotal():>15,}원")
        print(f"{'쿠폰 할인':<10} {self.discount():>15,}원")
        print(f"{'배송비':<10} {self.shipping():>15,}원")
        print(f"{'결제금액':<10} {self.total():>15,}원")
        print(line)



    def checkout(self):
        if self.is_empty(): return
        
       
        self.show() 
        #재고 감소 처리
        for p, q in self.items.items():
            p.stock -= q

        # 장바구니 비우기
        self.items.clear()
        self.coupon = None

        # 결제 성공여부 skip
        print("결제가 완료되었습니다. 감사합니다!!")

    #쿠폰 해보자고
    def apply_coupon(self, coupon):
        if self.coupon is not None:
            print("이미 쿠폰이 적용되어 있습니다.")
            return
        self.coupon = coupon
    #쿠폰 할인금액
    def discount(self):
        if self.coupon is None:
            return 0 
        return self.coupon.discount_amount(self.subtotal())
    




#--------------------------------------------------------
# 테스트 코드
#--------------------------------------------------------
# 제품 인스턴스 생성 
tumbler = Product("텀블러", 15_000, 10)
earphone = Product("무선 이어폰", 89_000, 3)
usbhub = Product("USB 허브", 20_000, 5)

# 카트 인스턴스 생성
cart = Cart()
cart.add(tumbler, 3)
cart.add(earphone, 2)
cart.add(usbhub, 4)
coupon = PercentCoupon(0.1, 5_000)
coupon = FixedCoupon(5_000, 30_000)
cart.apply_coupon(coupon)
cart.apply_coupon(coupon)
cart.checkout()


print(tumbler)
print(earphone)
print(usbhub)