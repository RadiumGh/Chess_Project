from django.shortcuts import *
from django.http import *
from .models import User
from django.core.mail import send_mail
from . import AI
from random import *

username = 'reza'

def home(request):
	return render(request, "chess/home.html", {'login_error': "", 'register_error': ""})


def login(request):
	error = ""
	try:
		users = User.objects.filter(email=request.POST['email'].lower(), password=request.POST['password'])
		if(not users):
			error = "No user found!"
			raise "Error"
		else:
			user = users[0]
			if(user.is_active):
				request.session['username'] = user.username
				request.session['turn'] = 'me'
				return HttpResponseRedirect("/chess/game")
			else:
				error = "User is not Activated Yet :| !!"
				raise "Error"
	except:
		return render(request, "chess/home.html", {'login_error': error, 'register_error': ""})


def register(request):
	global username

	if(not User.objects.filter(username=request.POST['username']) and not User.objects.filter(email=request.POST['email'])):
		user = User(username=request.POST['username'].lower(), password=request.POST['password'], email=request.POST['email'].lower(),
			board="RNBQKBNR.PPPPPPPP.eeeeeeee.eeeeeeee.eeeeeeee.eeeeeeee.pppppppp.rnbqkbnr")
		
		activation_code = repr(randint(100000, 1000000))
		user.activation_code = activation_code
		user.save()

		request.session['username'] = user.username
		request.session['turn'] = 'me'

		send_mail('Activation Code', 
			'Activation Code : ' + activation_code +'\nUsername : ' + user.username,
			'icp95.project@gmail.com',
			[user.email])

		return render(request, 'chess/home.html', {'register_error': "Activation Code was Sent to your mail !", 'login_error': "", 'active_error': ""})

	else:
		return render(request, 'chess/home.html', {'register_error': "username or email already Exists !", 'login_error': "", 'active_error': ""})


def sign_out(request):
	request.session['uername'] = ''
	request.session['turn'] = 'me'
	return render(request, 'chess/home.html')


def active(request):
	users = User.objects.filter(username=request.POST['username'])
	if(users):
		user = users[0]
		entered_code = request.POST['code']
		user_code = user.activation_code

		if(repr(user_code) == repr(entered_code)):
			if(user.is_active):
				return render(request, 'chess/home.html', {'active_error': "User has been Activated Before !", 'register_error': "", 'login_error': ""})	
			
			user.is_active = True
			user.save()
			request.session['username'] = user.username
			request.session['turn'] = 'me'
			message = ""

			return HttpResponseRedirect('/chess/game')
		else:
			return render(request, 'chess/home.html', {'active_error': "Activation Code Doesn't match !!! :|", 'register_error': "", 'login_error': ""})
	else:
		return render(request, 'chess/home.html', {'active_error': "No User Found !!", 'register_error': "", 'login_error': ""})


message = ""


def game(request):
	global message

	user = User.objects.get(username=request.session['username'])
	# user.board = "RNBQKBNR.PPPPPPPP.eeeeeeee.eeeeeeee.eeeeeeee.eeeeeeee.pppppppp.rnbqkbnr"
	# user.save()
	state=user.board
	loses = user.loses
	wins = user.wins
	
	users = User.objects.all()
	scores_tpl_list = []
	for u in users:
		scores_tpl_list.append((u.wins - u.loses, u.username))
	scores_tpl_list.sort()

	scores_strs = []
	for s in scores_tpl_list:
		scores_strs .append(str(s[1]) + " ==> " + str(s[0]))

	state_list = state.split('.')
	board_imgs = []
	for row in state_list:
		tmp = []
		for piece in row:
			tmp.append(piece+".png")
		board_imgs.append(tmp)

	turn = request.session['turn']
	return render(request, 'chess/game.html', {'state': state_list, 'board_imgs': board_imgs, 'message': message, 'turn': turn, 'wins': wins, 'loses': loses,
												 'scores': scores_strs, 'username': user.username })


def move(request):
	global message

	turn = request.session['turn']
	user = User.objects.get(username=request.session['username'])

	if(turn == 'me'):
		move = request.POST['move'].lower().strip()
		if(move == "reset"):
			user.board = "RNBQeBNR.qqqqqKqq.qqqqqqqq.eeeeeeee.eeeeeeee.eeeeeeee.pppppppp.rnbqkbnr"
			user.save()

			message = "Game has been reseted !"
			return HttpResponseRedirect('/chess/game')
		else:
			ai_obj = AI.AI(user.board)
			
			if(move == "safe"):
				#return HttpResponse(ai_obj.state_is_safe(ai_obj.state_mat, True))
				ls = ai_obj.generate_next_possible_safe_states(ai_obj.state_mat, True)
				string = ""
				for l in ls:
					string += str(l) + '\n enddddd  '
				return HttpResponse(string)
			try:
				if(ai_obj.move_is_valid(move)):	
					mv_tuples = ai_obj.return_move_tuples(move)
					new_state = ai_obj.update_state_with_move(mv_tuples[0], mv_tuples[1], ai_obj.state_mat, False)
					if(not ai_obj.state_is_safe(new_state, False)):
						massage = "You cannot do that ! :|"
						return HttpResponseRedirect('/chess/game')
					user.board = ai_obj.convert_mat_to_str(new_state)
					user.save()

					if(not ai_obj.generate_next_possible_safe_states(new_state, True)):
						request.session['turn'] = 'me'
						message = "YOU WON !"
						user.wins += 1
						user.save()
						return HttpResponseRedirect('/chess/game')
					
					if(not ai_obj.generate_next_possible_safe_states(new_state, False)):
						request.session['turn'] = 'me'
						message = "YOU LOST !"
						user.loses += 1
						user.save()
						return HttpResponseRedirect('/chess/game')

					request.session['turn'] = 'ai'
					message = ""
					return HttpResponseRedirect('/chess/game')
				else:
					message = "Move is not valid !"
					return HttpResponseRedirect('/chess/game')
			except:
				message = "Move is not valid !"
				return HttpResponseRedirect('/chess/game') 
	else:
		ai_obj = AI.AI(user.board)
		new_state = ai_obj.convert_str_to_mat(ai_obj.board)

		AI_move = ai_obj.alpha_beta(new_state, 4, -1000000, 1000000, 1)[1]

		if(not ai_obj.generate_next_possible_safe_states(AI_move, True)):
			request.session['turn'] = 'me'
			user.wins += 1
			user.save()
			message = "YOU WON !"
			return HttpResponseRedirect('/chess/game')
				
		if(not ai_obj.generate_next_possible_safe_states(AI_move, False)):
			request.session['turn'] = 'me'
			message = "YOU LOST !"
			user.loses += 1
			user.save()
			return HttpResponseRedirect('/chess/game')

		user.board = ai_obj.convert_mat_to_str(AI_move)
		user.save()
		message = ""
		request.session['turn'] = 'me'
		return HttpResponseRedirect('/chess/game')
	


