def getGreetingMessage():
  messsage = 'Seja bem-vindo(a)! Use um dos seguintes comandos para começar:'
  messsage += '\n\n/ajustar - Ajuste o seu horário de ler o texto diário.'
  messsage += '\n\n/ler - Leia agora o texto para hoje.'

  return messsage

def getAdjustingScheduleMessage():
  message = 'Ok, vamos ajustar seu horário. '
  message += 'Escolha que horas você gostaria de receber o texto diário:'

  return message

def getUnknownScheduleOptionMessage():
  message = 'Desculpe, não entendi sua mensagem. Tente novamente.'
  return message

def getNotInSchedulesMessage():
  message = 'Ops, por enquanto não contemplo esse horário. 🥲'
  return message

def getSetInScheduleMessage():
  message = 'Ok, a partir de hoje você receberá o texto diário às %s horas. 😃🙏'
  return message

def getUnknownCommandMessage():
  message = 'Desculpe, não entendi o que você quis dizer. Tente outro comando.'
  return message