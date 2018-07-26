from flask import url_for


def paginate(total,page,amount,end_point,**kwargs):
    prev = None
    next = None
    if total < amount:
        page = 1
    elif (page - 1) * amount > total > amount:
        page = 1
        next = url_for(end_point, page=page + 1, amount=amount,**kwargs)
    elif total > amount and total > (page - 1) * amount:
        if page == 1:
            next = url_for(end_point, page=page + 1, amount=amount, **kwargs)
        elif total > page * amount:
            prev = url_for(end_point, page=page - 1, amount=amount, **kwargs)
            next = url_for(end_point, page=page + 1, amount=amount, **kwargs)
        else:
            prev = url_for(end_point, page=page - 1, amount=amount, **kwargs)

    return page,prev,next