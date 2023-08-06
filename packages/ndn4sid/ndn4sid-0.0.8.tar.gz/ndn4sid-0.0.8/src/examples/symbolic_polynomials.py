from ndn4sid import polynomials


def main():
    # Define 3 random monomials.
    a = polynomials.Monomial(1,(1,2,3))  
    b = polynomials.Monomial(2,(2,2,3))  
    c = polynomials.Monomial(3,(2,2,3))  

    # Define a polynomial containing 3 monomials a,b and c.
    p = polynomials.Polynomial([a,b,c])
    # Perform some calculations
    pp = p+p-3*p
    p2 = (pp**2).simplify()
    # Calculate the derivative
    p_d = p2.d(0,2)
    print(p_d)



if __name__ == "__main__":
    main()