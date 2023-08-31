    
def member(name, mbti, *args):
    print(f"이름: {name}")
    print(f"MBTI: {mbti}")
    print(f"직업: {args}")
    
    
def member2(name, mbti, *args, **kwargs):
    print(f"이름: {name}")
    print(f"MBTI: {mbti}")
    print(f"직업: {args}")
    email = kwargs["email"] or None
    interest = kwargs["interest"] or None
    if email:
        print(email)
    if interest:
        print(interest)
    return True