from constants import *
import pygame as pg
import pygame_widgets
from pygame_widgets.button import Button


menu_running = True
return_to_menu = False



def menu_stop(): #stops running the menu
    global menu_running
    menu_running =False
    global return_to_menu
    return_to_menu = False

def menu_restart(): # when the menu button is pressed in the intermission
    global menu_running 
    menu_running = False
    global return_to_menu
    return_to_menu = True # Procedure which sets return_to_menu to be true

def menu_loading(font,canvas,button,x,y):
    pygame_widgets.button.Button.hide(button)   
    loading_text = font.render("LOADING...",True, "#000000","#FFFFFF" )    
    canvas.blit(loading_text,(x,y))
    menu_stop()
    
#instructions
def instructions_box(canvas):
    #font for the instructions
    instruction_font = pg.font.SysFont("Gadugi",28, True)
    #creates a rectangle in the bottom right corner with width 400 and height 299 pixels.
    pg.draw.rect(canvas, "#FFFFFF", pg.Rect(780,450,400,200)) 
    # text for all the instructions       
    instructions_1 = instruction_font.render("Use W A S D keys to move.",True, "#000000" )
    instructions_2 = instruction_font.render("Avoid the red enemies.",True, "#000000" )
    instructions_3 = instruction_font.render("Collect as many yellow ",True, "#000000" )
    instructions_4 = instruction_font.render("items as possible.",True, "#000000" )
    # adds the text to the canvas
    canvas.blit(instructions_1,(800,450))    
    canvas.blit(instructions_2,(800,500)) 
    canvas.blit(instructions_3,(800,550)) 
    canvas.blit(instructions_4,(800,600)) 

#main menu
def menu_create():
    pg.init()
    return_to_menu = False

    
    clock = pg.time.Clock()
    pg.font.get_fonts()
    canvas = pg.display.set_mode(DIMENSIONS)
    canvas.fill(BG)
    pg.display.set_caption("Spoiled Oil")

    ##font
    title_font = pg.font.SysFont("Gadugi",112, True) # font for title
    main_font = pg.font.SysFont("Gadugi",72, True) # Font used in everything else. creates a font with bold True
    
    #title text
    title = title_font.render(" SPOILED OIL ",True, "#000000", "#FFFFFF")
    canvas.blit(title,(50,50))
    
    
    ##w key text
    w_key = main_font.render(" W ",True, "#000000", "#FFFFFF")
    w_key_Rect = w_key.get_rect()
    w_key_Rect.center = (1050,100)
    canvas.blit(w_key,w_key_Rect)
    
    ##d key text
    d_key = main_font.render(" D ",True, "#000000", "#FFFFFF")
    d_key_Rect = d_key.get_rect()
    d_key_Rect.center = (1150,220)
    canvas.blit(d_key,d_key_Rect)
    
    ##s key text
    s_key = main_font.render(" S ",True, "#000000", "#FFFFFF")
    s_key_Rect = s_key.get_rect()
    s_key_Rect.center = (1050,220)
    canvas.blit(s_key,s_key_Rect)
    
    ##a key text
    a_key = main_font.render(" A ",True, "#000000", "#FFFFFF")
    a_key_Rect = a_key.get_rect()
    a_key_Rect.center = (950,220)
    canvas.blit(a_key,a_key_Rect)
    
    #play button using pygame_widgets
    x=50
    y=250
    start_button = Button(
        canvas,
        x, # x
        y, # y
        350, # width
        150, # height
        text = "PLAY",
        font = title_font,
        hoverColour = HOVER_BUTTON, #colour when mouse cursor is hovered over
        inactiveColour = BUTTON_COLOUR, #default colour
        textColour = (0,0,0), 
        onClick = lambda :menu_loading(title_font,canvas,start_button,x,y) #when clicked, adds loading text
    
    
    )    
    # quit text button
    exit_button = Button(
        canvas,
        50, # x
        450, # y
        350, # width
        150, # height
        text = "QUIT",
        font = title_font,
        hoverColour = HOVER_BUTTON,
        inactiveColour = BUTTON_COLOUR,
        textColour = (0,0,0),
        onClick = lambda :pg.quit() #quits game

    
    )   

    pg.display.update()
    
    #'?' button
    instructions_button = Button(
        canvas,
        1180, # x
        600, # y
        80, # width
        100, # height
        text = "?",
        font = title_font,
        hoverColour = HOVER_BUTTON,
        inactiveColour = BUTTON_COLOUR,
        textColour = (0,0,0),
        onClick = lambda :instructions_box(canvas) # adds the box and text to the canvas

    
    )   
        

    while menu_running:
        events = pg.event.get()
        pygame_widgets.update(events)
        pg.display.update()
        if menu_running == False: #hides the buttons the menu has been exited
            pygame_widgets.button.Button.hide(start_button) 
            pygame_widgets.button.Button.hide(exit_button)
            pygame_widgets.button.Button.hide(instructions_button)
        clock.tick(60) # wait 16.7ms
        for event in pg.event.get(): # searches the events
            if event.type == pg.QUIT: #if the user presses the close the program will close
                pg.quit()


#menu screen between levels
def intermission(highScores): 
    pg.init()
    global menu_running
    clock = pg.time.Clock()
    pg.font.get_fonts()
    canvas_2 = pg.display.set_mode(DIMENSIONS)
    canvas_2.fill(BG)
    pg.display.set_caption("Spoiled Oil")
    #assigning fonts
    leaderBoard_font = pg.font.SysFont("Gadugi",48, True)
    continue_font = pg.font.SysFont("Gadugi",112,True)
    #BUTTONS
    x = 50
    y = 50
    #continue button
    advance_button = Button( #continue to next level
        canvas_2,
        x,
        y,
        650,
        150,
        text = "CONTINUE",
        font = continue_font,
        hoverColour = HOVER_BUTTON,
        inactiveColour = BUTTON_COLOUR,
        textColour = (0,0,0),
        onClick = lambda :menu_stop() # closes the menu
    
    
    )
    # main menu button
    menu_button = Button( 
        canvas_2,
        900, # x
        50, # y
        350, # width
        150, # height
        text = "MENU",
        font = continue_font,
        hoverColour = HOVER_BUTTON,
        inactiveColour = BUTTON_COLOUR,
        textColour = (0,0,0),
        onClick = lambda :menu_restart()  #returns to main menu
    )
    
    
    #adding scores to the leader board
 
    highScores = open("highScores.txt", "r")
    lines = highScores.readlines()

    ##adds white rectangle where the scores will be (w=400, h = 325 pixels)
    pg.draw.rect(canvas_2, "#FFFFFF", pg.Rect(50,300,400,325))
    #adds the text 'leaderboard' at the top of this rectangle
    leaderBoard = leaderBoard_font.render("LEADERBOARD",True, "#000000")    
    canvas_2.blit(leaderBoard,(75,300))  
    ##searches the scores
    for i in range(len(lines)):
        if str(lines[i])[0] == "#": # if the score starts with #,
            score_1 = leaderBoard_font.render((str(i+1)+". " +str(lines[i].strip("\n")[1:])),True, "#00FF00") # The text is green
            canvas_2.blit(score_1,(75,350 + 50*i)) # further down the higher i is
        else: #if score is not new.
            score_1 = leaderBoard_font.render((str(i+1)+". " +str(lines[i].strip("\n"))),True, "#000000") #text is black.
            canvas_2.blit(score_1,(75,350 + 50*i))

      
        
    highScores.close()
     
        

    


    pg.display.update()
    
    while menu_running:
  
        events = pg.event.get()
        pygame_widgets.update(events)
        pg.display.update()
        if menu_running == False:
            pygame_widgets.button.Button.hide(advance_button) #hides the buttons when the menu closes.
            pygame_widgets.button.Button.hide(menu_button)        

            if return_to_menu == True: #The way to link back to the main menu
                menu_running = True
                menu_create()

        for event in pg.event.get(): #searches all the events
            if event.type == pg.QUIT: #if the user presses the x, the program will close
                pg.quit()        
        clock.tick(60)
    