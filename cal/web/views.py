from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from web.models import User, Expense,Income  # adjust imports as per your actual models
from datetime import datetime

@csrf_exempt
def submit_expense(request):
    """User submits an expense"""
    if request.method == "POST":
        token = request.POST.get('token')
        amount = request.POST.get('amount')
        text = request.POST.get('text')
        date_str = request.POST.get('date')  # optional custom date

        if not token or not amount or not text:
            return JsonResponse({'status': 'error', 'message': 'Missing required fields'}, status=400)

        try:
            this_user = User.objects.get(token__token=token)
        except User.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Invalid Token'}, status=400)

        # handle date
        if date_str:
            try:
                expense_date = datetime.strptime(date_str, "%Y-%m-%d")
            except ValueError:
                return JsonResponse({'status': 'error', 'message': 'Invalid date format. Use YYYY-MM-DD'}, status=400)
        else:
            expense_date = datetime.now()

        # Validate amount
        try:
            amount_value = float(amount)
        except ValueError:
            return JsonResponse({'status': 'error', 'message': 'Amount must be numeric'}, status=400)

        # Create expense
        Expense.objects.create(user=this_user, amount=amount_value, text=text, date=expense_date)

        return JsonResponse({'status': 'ok', 'user': this_user.username})

    return JsonResponse({'status': 'error', 'message': 'POST required'}, status=405)


@csrf_exempt
def submit_income(request):
    """User submits an income"""
    if request.method == "POST":
        token = request.POST.get('token')
        amount = request.POST.get('amount')
        text = request.POST.get('text')
        date_str = request.POST.get('date') # optional custom date

        if not token or not amount or not text:
            return JsonResponse({'status':'error','message':'Missing required fields'},status=400)
        
        try:
            this_user = User.objects.get(token__token=token)
        except User.DoesNotExist:
            return JsonResponse({'status':'error','message':'Invalid Token'},status=400)
        
        #handle date
        if date_str:
            try:
                expnse_date = datetime.strptime(date_str,"%Y-%m-%d")
            except ValueError:
                return JsonResponse({'status':'error','message':'Invalid date format. Use YYYY-MM-DD'},status = 400)
        else:
            expnse_date = datetime.now()

        # Validate amount
        try:
            amount_value = float(amount)
        except ValueError:
            return JsonResponse({'status':'error','message':'Amount must be numeric'},status=400)
        
        # Create expense
        Income.objects.create(user=this_user,amount=amount_value,text=text,date=expnse_date)

        return JsonResponse({'status':'ok','user':this_user.username})
    
    return JsonResponse({'status':'error','message':'POST required'},status=405)































