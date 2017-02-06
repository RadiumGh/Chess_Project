from django.shortcuts import *
from django.http import *
from .models import User
from django.core.mail import send_mail
from . import AI

username = 'reza'

def home(request):
	#if(request.session.get('username', 0) == 0):
	return render(request, "chess/home.html", {'login_error': "", 'register_error': ""})
	#else:
	#return HttpResponseRedirect("/chess/game")


def login(request):
	try:
		user = User.objects.get(email=request.POST['email'].lower(), password=request.POST['password'])
		request.session['username'] = user.username
		request.session['turn'] = 'me'
		return HttpResponseRedirect("/chess/game")
	except:
		return render(request, "chess/home.html", {'login_error': "No user found!", 'register_error': ""})


def register(request):
	global username

	if(not User.objects.filter(username=request.POST['username']) and not User.objects.filter(email=request.POST['email'])):
		user = User(username=request.POST['username'].lower(), password=request.POST['password'], email=request.POST['email'].lower(),
			board="RNBQKBNR.PPPPPPPP.eeeeeeee.eeeeeeee.eeeeeeee.eeeeeeee.pppppppp.rnbqkbnr")
		
		activation_code = '123456789'
		user.activation_code = activation_code
		user.save()

		request.session['username'] = user.username
		request.session['turn'] = 'me'
		send_mail('Activation Code', 
			'Activation Code : ' + activation_code,
			 'icp95.project@gmail.com', [user.email])

		message = ""
		return HttpResponseRedirect('/chess/game')
	else:
		return render(request, 'chess/home.html', {'register_error': "username or email already Exists !", 'login_error': ""})

def active(request):
	user = User.objects.get(username=request.POST['username'])
	entered_code = request.POST['code']

	user_code = user.activation_code
	if(repr(user_code) == repr(entered_code)):
		user.is_active = True
	# else:
	# 	return render(request, t)


message = ""
turn = ""

def game(request):
	global message

	user = User.objects.get(username=request.session['username'])
	# user.board = "RNBQKBNR.PPPPPPPP.eeeeeeee.eeeeeeee.eeeeeeee.eeeeeeee.pppppppp.rnbqkbnr"
	# user.save()
	state=user.board
	state_list = state.split('.')
	board_imgs = []
	for row in state_list:
		tmp = []
		for piece in row:
			tmp.append(piece+".png")
		board_imgs.append(tmp)

	turn = request.session['turn']
	return render(request, 'chess/game.html', {'state': state_list, 'board_imgs': board_imgs, 'message': message, 'turn': turn})

def move(request):
	global message

	turn = request.session['turn']
	user = User.objects.get(username=request.session['username'])

	if(turn == 'me'):
		move = request.POST['move']
		if(move == "reset"):
			user.board = "RNBQeBNR.qqqqeqKq.qqqqqeqq.eeeeeeee.eeeeeeee.eeeeeeee.pppppppp.rnbqkbnr"
			user.save()

			message = "Game has been reseted !"
			return HttpResponseRedirect('/chess/game')
		else:
			ai_obj = AI.AI(user.board)
			
			if(move == "safe"):
				return HttpResponse(ai_obj.state_is_safe(ai_obj.state_mat, True))
				#return HttpResponse(ai_obj.generate_next_possible_safe_states(ai_obj.state_mat, True))

			if(ai_obj.move_is_valid(move)):	
				mv_tuples = ai_obj.return_move_tuples(move)
				new_state = ai_obj.update_state_with_move(mv_tuples[0], mv_tuples[1], ai_obj.state_mat, False)
				
				user.board = ai_obj.convert_mat_to_str(new_state)
				user.save()

				# if(not ai_obj.generate_next_possible_safe_states(new_state, True)):
				# 	request.session['turn'] = 'me'
				# 	message = "YOU WON !"
				# 	return HttpResponseRedirect('/chess/game')
				
				if(not ai_obj.generate_next_possible_safe_states(new_state, False)):
					request.session['turn'] = 'me'
					message = "YOU LOST !"
					return HttpResponseRedirect('/chess/game')

				request.session['turn'] = 'ai'
				return HttpResponseRedirect('/chess/game')
			else:
				message = "Move is not valid !"
				return HttpResponseRedirect('/chess/game') 
	else:
		ai_obj = AI.AI(user.board)
		new_state = ai_obj.convert_str_to_mat(ai_obj.board)

		AI_move = ai_obj.mini_max(new_state, 4, -10000, 10000, True)[1]

		if(not ai_obj.generate_next_possible_safe_states(AI_move, True)):
			request.session['turn'] = 'me'
			message = "YOU WON !"
			return HttpResponseRedirect('/chess/game')
				
		if(not ai_obj.generate_next_possible_safe_states(AI_move, False)):
			request.session['turn'] = 'me'
			message = "YOU LOST !"
			return HttpResponseRedirect('/chess/game')

		user.board = ai_obj.convert_mat_to_str(AI_move)
		user.save()
		message = ""
		request.session['turn'] = 'me'
		return HttpResponseRedirect('/chess/game')
	


