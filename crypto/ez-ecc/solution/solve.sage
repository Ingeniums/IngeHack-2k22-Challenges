from sage.all import *



F = Zmod(139)
x = F(36)
y = F(80)
x1 = F(7)
y1 = F(43)
a = ((y1^2 -x1^3 - y^2 +x^3) / (x1-x))
b = ((y^2-x^3-a*x))

def SmartAttack(P,Q,p):
    E = P.curve()
    Eqp = EllipticCurve(Qp(p, 2), [ ZZ(t) + randint(0,p)*p for t in E.a_invariants() ])

    P_Qps = Eqp.lift_x(ZZ(P.xy()[0]), all=True)
    for P_Qp in P_Qps:
        if GF(p)(P_Qp.xy()[1]) == P.xy()[1]:
            break

    Q_Qps = Eqp.lift_x(ZZ(Q.xy()[0]), all=True)
    for Q_Qp in Q_Qps:
        if GF(p)(Q_Qp.xy()[1]) == Q.xy()[1]:
            break

    p_times_P = p*P_Qp
    p_times_Q = p*Q_Qp

    x_P,y_P = p_times_P.xy()
    x_Q,y_Q = p_times_Q.xy()

    phi_P = -(x_P/y_P)
    phi_Q = -(x_Q/y_Q)
    k = phi_Q/phi_P
    return ZZ(k)

# Curve parameters --> Replace the next three lines with given values
p = 92517377285964712700402768201686388458777796513029661121387518457855305003887 
a = 38797243845245332525942134691000380783420213418502850949997762221448580551178
b = 90535513088702227288147691079962260896031851928073931499601588803955767119399

# Define curve
E = EllipticCurve(GF(p), [a, b])
assert(E.order() == p)

# Replace the next two lines with given values
P1 = E(57516588543456146838199882006427760473316432435743787681085541042704497002386 , 40968551252076601267516886191968225258642079470095088696874521610682853644694)
P2 = E(24816742899058014660491715684544746934403517722825986685547561050157776456982 , 24576908297795652697606612249696595739976335097722967340743949068201091050924)

print(SmartAttack(P1,P2,p))





p = 902218707944511428508944163907946761763022811
a = 902218707944511428508944163907946761763022810 
b = 0

# Define curve
E = EllipticCurve(GF(p), [a, b])
order = E.order()
print(is_prime(order))

# Replace the next two lines with given values
P1 = E(208936452217600192180393827102323580818439050 , 212950229796201133508018850583402578730923913)
P2 = E(700352764988553493480813431886677029352850747 , 380473098128032723375022309139277511036504749)
n = P1.order()

k = 1
while (p**k - 1) % order:
	k += 1

K.<a> = GF(p**k)
EK = E.base_extend(K)
PK = EK(P2)
GK = EK(P1)

while True:
	R = EK.random_point()
	m = R.order()
	d = gcd(m,n)
	Q = (m//d)*R
	if n / Q.order() not in ZZ:
		continue
	if n == Q.order():
		break

print('Computing pairings')
alpha = GK.weil_pairing(Q,n)
beta = PK.weil_pairing(Q,n)

print("Computing the log")
dd = beta.log(alpha)
print(dd)

