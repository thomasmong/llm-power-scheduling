from ctypes import alignment
from manim import *

###
# This is a demo video that explains the ashem project
# It shows the problem to solve and the proposed solution

class Intro(Scene):

    def construct(self):
        title = "ASHEM Project"
        subtitle = "A Smart Home optimizer assistant based on LLM"
        Title = Text(title,font="Satoshi Medium",font_size=80).shift(UP)
        Subtitle = Paragraph("A Smart Home optimizer assistant","based on LLM",font="Satoshi Medium",alignment='center').next_to(Title,DOWN)
        self.play(Write(Title))
        self.play(Write(Subtitle))
        self.wait(3)

        self.play(Unwrite(Subtitle),Unwrite(Title),run_time=1)

class Situation(Scene):

    global evSVG, personSVG
    evSVG = SVGMobject("img/ev.svg",width=4).to_corner(RIGHT+DOWN).shift(LEFT+UP)
    personSVG = SVGMobject("img/person.svg",height=1.8).to_corner(LEFT+DOWN).shift(RIGHT+1.5*UP)

    def construct(self):
        
        
        personShruggingSVG = SVGMobject("img/shrugging.svg",height=1.8).move_to(personSVG.get_center())
        questionmarkSVG = SVGMobject("img/questionmark.svg",width=0.4).next_to(personSVG,UP)
        
        bubble = SVGMobject("img/bubble.svg",width=5).next_to(personSVG,RIGHT).shift(2*UP)
        # Question on top of the bubble
        question = Paragraph("How should I charge","my EV in order to","reduce the costs?",line_spacing=1,font="Satoshi",font_size=25,alignment='center').move_to(bubble.get_center()).shift(0.3*UP+0.25*RIGHT)
        self.play(FadeIn(personSVG),FadeIn(evSVG))
        self.play(Write(bubble),Write(question))
        self.play(FadeOut(personSVG),FadeIn(personShruggingSVG),run_time=0.4)
        self.play(FadeIn(questionmarkSVG))
        # Emphasize the question
        self.play(Wiggle(questionmarkSVG),run_time=0.5)
        self.wait(1)

        # Fade out bubble and question + back to normal person
        self.play(Unwrite(bubble),Unwrite(question),FadeOut(questionmarkSVG),FadeOut(personShruggingSVG),FadeIn(personSVG),run_time=0.6)
    
class AssistantSolution(Scene):

    global robotSVG
    robotSVG = SVGMobject("img/robot.svg",height=1.8).to_edge(DOWN).shift(1.5*UP)

    def construct(self):
        # Shrink the EV
        self.add(evSVG, personSVG)

        self.play(evSVG.animate.set_height(1.4).to_corner(RIGHT+DOWN).shift(LEFT+1.5*UP))

        # Add the assistant
        robotTitle = Text("Optimizer assistant",font="Satoshi Medium",font_size=25).next_to(robotSVG,DOWN)
        robot = Group(robotSVG,robotTitle)
        self.play(GrowFromCenter(robot))
        self.wait(1)

        # User request
        bubble = SVGMobject("img/bubble_basic.svg",width=4).next_to(personSVG,RIGHT).shift(2.2*UP)
        request = Paragraph("Charge my EV","by 7AM but","reduce the costs",line_spacing=1,font="Satoshi",font_size=25,alignment='center').move_to(bubble.get_center()).shift(0.3*UP+0.18*RIGHT)
        self.play(Write(bubble),Write(request))
        self.wait(1)

        # Assistant processing
        # Move request to the assistant while fading
        self.play(Unwrite(bubble))
        self.play(FadeOut(request,target_position=robotSVG,scale=0.2))
        self.play(Wiggle(robotSVG,run_time=.8))
        self.play(Wiggle(robotSVG,run_time=.8))
        self.play(Flash(robotSVG,flash_radius=1,num_lines=10,run_time=.8))

        # Assistant response
        # Create bar chart
        yvalues = np.array([5,7,6,6,5,4,2])
        colors = [BLUE]*len(yvalues)
        axes = BarChart(yvalues,bar_width=1,bar_colors=colors,y_axis_config={"include_numbers":False}).set(width=3).next_to(robotSVG,0.7*RIGHT).shift(1.7*UP)
        axes.get_y_axis().set(includes_numbers=False)
        xlabel = axes.get_x_axis_label(Tex("Hours").scale(0.7),direction=DOWN,edge=DOWN)
        ylabel = axes.get_y_axis_label(Tex("Power").scale(0.7).rotate(90*DEGREES),direction=LEFT,edge=LEFT)
        full_ax = VGroup(axes,xlabel,ylabel)
        self.play(FadeIn(full_ax,target_position=robotSVG))
        self.wait(2)
        self.play(FadeOut(full_ax,target_position=evSVG, scale=0.2))
        self.wait(1)

        # Remove everything except the assistant
        self.play(FadeOut(evSVG),FadeOut(personSVG),FadeOut(robotTitle),robotSVG.animate.scale(0.25).to_edge(UP))
    

class AssistantDetail(MovingCameraScene):

    global MyOrange, MyPurple
    MyOrange = ManimColor("#F4AA40")
    MyPurple = ManimColor("#6A33CD")

    def construct(self):
        robotSVG.scale(0.25).to_edge(UP)
        self.add(robotSVG)
        frame = ScreenRectangle(height=6.4).next_to(robotSVG,DOWN)
        self.play(Create(frame))

        ## Whole diagram

        # Classifier
        classifierTitle = Paragraph("LLM-based intent\nrecognition agent",line_spacing=1, alignment='center',font="Satoshi Medium",font_size=30).scale(0.4)
        classifierBlock = SurroundingRectangle(classifierTitle,corner_radius=0.2,color=MyOrange,buff=MED_SMALL_BUFF).set_fill(MyOrange,0.4)
        classifier = VGroup(classifierBlock,classifierTitle)
        # Parser
        parserTitle = Paragraph("LLM-based parameter\nidentification agent",line_spacing=1, alignment='center',font="Satoshi Medium",font_size=30).scale(0.4)
        parserBlock = SurroundingRectangle(parserTitle,corner_radius=0.2,color=MyPurple,buff=MED_SMALL_BUFF).set_fill(MyPurple,0.4)
        parser = VGroup(parserBlock,parserTitle)

        # Smart Meter
        #smartMeterTitle = Text("Smart Meter",font="Satoshi Medium",font_size=30).scale(0.4)
        #smartMeterBlock = SurroundingRectangle(smartMeterTitle,corner_radius=0.2,color=MyPurple,buff=MED_SMALL_BUFF).set_fill(MyPurple,0.4)
        #smartMeter = VGroup(smartMeterBlock,smartMeterTitle)

        # Solver
        solverTitle = Paragraph("LLM-based\nOP solver",line_spacing=1, alignment='center',font="Satoshi Medium",font_size=30).scale(0.4)
        solverBlock = SurroundingRectangle(solverTitle,corner_radius=0.2,color=BLUE,buff=MED_SMALL_BUFF).set_fill(BLUE,0.4)
        solver = VGroup(solverBlock,solverTitle)


        # Arange blocks
        schema = VGroup(classifier,parser,solver).arrange(RIGHT,buff=1.2).center().shift(DOWN)
        self.play(FadeIn(schema))


        self.camera.frame.save_state()
        self.play(self.camera.frame.animate.move_to(classifier).shift(UP).set(width=6))

        ## Classifier step
        # Add the request
        req1 = Text("Charge my EV",font="Satoshi",font_size=30).scale(0.3)
        req2 = Text("by 7AM but",font="Satoshi",font_size=30).scale(0.3)
        req3 = Text("reduce the costs",font="Satoshi",font_size=30).scale(0.3)
        request = VGroup(req1,req2,req3).arrange(DOWN,buff=0.08).next_to(classifier,1.8*LEFT)
        #request = Paragraph("Charge my EV","by 7AM but","reduce the costs",line_spacing=1,font="Satoshi",font_size=30,alignment='center').scale(0.3).next_to(classifier,1.8*LEFT)
        self.play(Write(request))
        # Arrow to classifier
        arrow = Arrow(request.get_right(),classifier.get_left(),buff=0.1)
        self.play(GrowArrow(arrow))
        self.wait(1)

        # Classifier processing
        frameClassifier = ScreenRectangle(height=1.5).next_to(classifier,UP)
        frameClassifier.set(stroke_width=1)
        self.play(FadeIn(frameClassifier,target_position=classifier, scale=0.2))

        requestFramed = request.copy()
        self.play(requestFramed.animate.move_to(frameClassifier.get_center()).scale(1.4))

        self.play(Indicate(requestFramed[-1]))
        self.play(FadeOut(requestFramed[0]),FadeOut(requestFramed[1]),requestFramed[-1].animate.move_to(frameClassifier.get_top()).scale(1.4).shift(0.4*DOWN))
        LPtext = Text("Linear Programming",font="Satoshi",font_size=30).scale(0.5).move_to(frameClassifier.get_bottom()).shift(0.4*UP)
        arrowProc = Arrow(requestFramed[-1].get_bottom(),LPtext.get_top(),buff=0.1)
        self.play(Write(LPtext),GrowArrow(arrowProc))

        arrowOP = Arrow(classifier.get_right()+0.15*UP,parser.get_left()+0.15*UP,buff=0.1,stroke_width=2,max_tip_length_to_length_ratio=0.1)
        classOP = Paragraph("Optimization Problem (OP)\nclass",line_spacing=1, alignment='center',font="Satoshi",font_size=30).scale(0.2).next_to(arrowOP,0.3*UP)
        self.play(GrowArrow(arrowOP),Write(classOP))

        genericLP = MathTex(r"\begin{aligned}\min_{x} &\ c^\top x \\\text{s.t.} &\ A x \leq b \\&\ A_\text{eq} x = b_\text{eq} \\&\ l \leq x \leq u \end{aligned}",font_size=30).scale(0.5).next_to(classifier,UP)
        self.play(FadeOut(requestFramed[-1]),FadeOut(frameClassifier),FadeOut(arrowProc),Write(genericLP),LPtext.animate.next_to(genericLP,UP))

        classLP = Text("LP",font="Satoshi",font_size=30).scale(0.4).next_to(arrowOP,0.3*UP)
        self.play(FadeOut(classOP),TransformMatchingShapes(LPtext,classLP))

        arrowReq = Arrow(classifier.get_right()+0.15*DOWN,parser.get_left()+0.15*DOWN,buff=0.1,stroke_width=2,max_tip_length_to_length_ratio=0.1)
        reqCopy = request.copy()
        req = Text("request",font="Satoshi",font_size=30).scale(0.4).next_to(arrowReq,0.3*DOWN)
        self.play(GrowArrow(arrowReq),Transform(reqCopy,req))

        self.play(self.camera.frame.animate.move_to(parser).shift(UP).set(width=6))
        self.wait(1)

        ## Parser step
        genericLPCopy = genericLP.copy().next_to(parser,5*UP).scale(0.8)
        self.play(FadeIn(genericLPCopy,target_position=classLP, scale=0.2))

        # Parser processing
        frameParser = ScreenRectangle(height=.9).next_to(parser,UP)
        frameParser.set(stroke_width=1)
        reqCopy = request.copy().move_to(frameParser.get_center())
        self.play(FadeIn(frameParser,target_position=parser, scale=0.2),FadeIn(reqCopy,target_position=req))

        self.play(reqCopy[0][:6].animate.set_color(BLUE))
        self.play(Indicate(reqCopy[0][:6],color=BLUE),run_time=0.5)
        
        #self.add(index_labels(genericLPCopy[0],label_height=0.06,background_stroke_width=0))
        ineq = genericLPCopy[0][15:23]
        energy = MathTex(r"A_\text{eq}x", r"= ",r"E\left(\text{SOC}=1\right)",font_size=30).scale(0.5).scale(0.8).move_to(ineq).align_to(ineq,LEFT).shift(0.01*DOWN).set_color_by_tex("E",BLUE)
        charge = reqCopy[0][:6].copy()
        self.play(Transform(ineq,energy),Transform(charge,energy[2],scale=0.2))

        self.play(reqCopy[0][:6].animate.set_color(WHITE))
        self.play(reqCopy[2][-5:].animate.set_color(YELLOW))
        self.play(Indicate(reqCopy[2][-5:],color=YELLOW),run_time=0.5)

        cVec = genericLPCopy[0][4:7]
        obj = MathTex(r"\text{prices}",r"^\top x",font_size=30).scale(0.5).scale(0.8).move_to(cVec).align_to(cVec,LEFT).shift(0.01*DOWN).set_color_by_tex("prices",YELLOW)
        costs = reqCopy[2][-5:].copy()
        self.play(Transform(cVec,obj),Transform(costs,obj[0],scale=0.2))

        
        self.play(reqCopy[2][-5:].animate.set_color(WHITE))

        self.play(reqCopy[1][2:5].animate.set_color(RED))
        self.play(Indicate(reqCopy[1][2:5],color=RED),run_time=0.5)
        am = reqCopy[1][2:5].copy()

        midLP = MathTex(r"\begin{aligned}\min_{x} &\ \text{prices}^\top \begin{pmatrix} x_1\\ \vdots\\ x_{10} \end{pmatrix} \\\text{s.t.} &\ \begin{pmatrix} 1 \cdots 1 \end{pmatrix} \begin{pmatrix} x_1\\ \vdots\\ x_{10} \end{pmatrix} = E\left(\text{SOC}=1\right) \\&\ 0 \leq x_1, \ldots , x_{10} \leq P_\text{max} \end{aligned}",font_size=30).scale(0.5).scale(0.5).move_to(genericLPCopy)
        #self.add(index_labels(midLP[0],label_height=0.06,background_stroke_width=0))
        midLP[0][4:10].set_color(YELLOW)
        midLP[0][51:59].set_color(BLUE)
        midLP[0][15].set_color(RED)
        midLP[0][20:22].set_color(RED)
        midLP[0][40].set_color(RED)
        midLP[0][45:47].set_color(RED)
        midLP[0][62].set_color(RED)
        midLP[0][69:71].set_color(RED)
        self.remove(costs,charge)
        self.play(TransformMatchingShapes(genericLPCopy,midLP),FadeOut(am,target_position=midLP, scale=0.2))
        self.play(FadeOut(reqCopy),FadeOut(frameParser),midLP.animate.scale(1.6).next_to(parser,UP))
        self.wait(1)

        arrowCall = Arrow(parser.get_right(),solver.get_left(),buff=0.1,stroke_width=2,max_tip_length_to_length_ratio=0.1)
        call = Text("complete OP",font="Satoshi",font_size=30).scale(0.4).next_to(arrowCall,0.3*UP)
        self.play(GrowArrow(arrowCall),Transform(midLP.copy(),call))
        self.wait(1)

        # Smart Meter step
        #self.play(self.camera.frame.animate.move_to(smartMeter).shift(UP).set(width=6))
        #self.wait(1)

        # Smart Meter processing
        #frameSmartMeter = ScreenRectangle(height=1.5).next_to(smartMeter,UP)
        #frameSmartMeter.set(stroke_width=1)
        #self.play(FadeIn(frameSmartMeter,target_position=smartMeter, scale=0.2))
        #midLPCopy = midLP.copy().move_to(frameSmartMeter.get_center()).set(height=1.2)
        #callCopy=call.copy()
        #self.play(ReplacementTransform(callCopy,midLPCopy))
        #self.add(index_labels(midLPCopy[0],label_height=0.04,background_stroke_width=0))


        #obj = midLPCopy[0][4:25]
        #objVec = MathTex(r"\begin{pmatrix} 0.24 \cdots 0.23 \end{pmatrix}",r"\begin{pmatrix} x_1\\ \vdots\\ x_{10} \end{pmatrix}",font_size=30).scale(0.8).scale(0.5).move_to(obj).align_to(obj,LEFT).set_color_by_tex("0.24",YELLOW)
        #objVec[1][4].set_color(RED)
        #objVec[1][9:11].set_color(RED)
        #self.remove(callCopy)
        #self.play(TransformMatchingShapes(obj,objVec))

        #energy = midLPCopy[0][51:59]
        #energyValue = MathTex(r"50",font_size=30).scale(0.5).scale(0.8).move_to(energy).align_to(energy,LEFT).set_color(BLUE)
        #self.play(TransformMatchingShapes(energy,energyValue))

        #powerMax = midLPCopy[0][72:]
        #powerMaxValue = MathTex(r"10",font_size=30).scale(0.5).scale(0.8).move_to(powerMax).align_to(powerMax,LEFT)
        #self.play(TransformMatchingShapes(powerMax,powerMaxValue))


        #finalLP = MathTex(r"\begin{aligned}\min_{x} &\ \begin{pmatrix} 0.24 \cdots 0.23 \end{pmatrix} \begin{pmatrix} x_1\\ \vdots\\ x_{10} \end{pmatrix} \\\text{s.t.} &\ \begin{pmatrix} 1 \cdots 1 \end{pmatrix} \begin{pmatrix} x_1\\ \vdots\\ x_{10} \end{pmatrix} = 50 \\&\ 0 \leq x_1, \ldots , x_{10} \leq 10 \end{aligned}",font_size=30).scale(0.8).scale(0.5).next_to(smartMeter,UP)
        #self.add(index_labels(finalLP[0],label_height=0.04,background_stroke_width=0))
        #finalLP[0][4:17].set_color(YELLOW)
        #finalLP[0][57:59].set_color(BLUE)
        #finalLP[0][21].set_color(RED)
        #finalLP[0][26:28].set_color(RED)
        #finalLP[0][46].set_color(RED)
        #finalLP[0][51:53].set_color(RED)
        #finalLP[0][62].set_color(RED)
        #finalLP[0][69:71].set_color(RED)
        #self.remove(obj,energy,powerMax,objVec,energyValue,powerMaxValue)
        #finalLP.set(height=midLPCopy.get_height()).move_to(midLPCopy).align_to(midLPCopy,LEFT)
        #self.add(finalLP)
        #self.remove(objVec,energyValue,powerMaxValue)
        #midLPCopy.set_opacity_by_tex("x",0)
        #self.play(FadeOut(midLPCopy[:4],run_time=0.001),FadeOut(midLPCopy[25:51],run_time=0.001),FadeOut(midLPCopy[59:72],run_time=0.001))
        #self.play(finalLP.animate.next_to(smartMeter,UP),FadeOut(frameSmartMeter))
        #self.wait(1)

        #arrowSolver = Arrow(smartMeter.get_right(),solver.get_left(),buff=0.1,stroke_width=2,max_tip_length_to_length_ratio=0.1)
        #finalOP = Text("Final OP",font="Satoshi",font_size=30).scale(0.4).next_to(arrowSolver,0.3*UP)
        #self.play(GrowArrow(arrowSolver),Transform(finalLP.copy(),finalOP,replace_mobject_with_target_in_scene=True))

        self.play(self.camera.frame.animate.move_to(solver).shift(UP).set(width=6))

        ## Solver step
        frameSolver = ScreenRectangle(height=1.5).next_to(solver,UP)
        frameSolver.set(stroke_width=1)
        midLPCopy = midLP.copy().move_to(frameSolver.get_center()).set(height=1.2)
        self.play(FadeIn(frameSolver,target_position=solver, scale=0.2),ReplacementTransform(call,midLPCopy))
        self.wait(0.5)

        ## Solver processing
        # Graphs
        # Bar chart Power
        yvalues = np.array([5,5,5,5,5,5,5,5,5,5])
        colors = [BLUE]*len(yvalues)
        axes = BarChart(yvalues,y_range=[0,12,5],y_length=5,bar_width=1,bar_colors=colors,bar_stroke_width=1,y_axis_config={'unit_size':1,'label_direction':LEFT}).set(width=1.885).move_to(frameSolver).shift(0.1*DOWN+0.1*LEFT)
        axes.set_z_index(-2)

        w = axes.coords_to_point(0,0)[0]-axes.coords_to_point(10,0)[0]


        prices = [0.24, 0.24, 0.23, 0.23, 0.22, 0.21, 0.21, 0.22, 0.22 ,0.23]
        pricesAx = Axes(x_range=[0,10,1],y_range=[0.2,0.25,0.01],tips=False,y_axis_config={'include_numbers':True, 'label_direction':RIGHT}).set(width=1.8).align_to(axes,RIGHT+DOWN)
        for (i,price) in enumerate(prices):
            #Create rectangle
            w = pricesAx.coords_to_point(i,0)[0]-pricesAx.coords_to_point(i+1,0)[0]
            h = pricesAx.c2p(0,price)[1]-pricesAx.c2p(0,0.2)[1]
            rect = Rectangle(width=w,height=h,color=YELLOW,stroke_width=1,fill_opacity=0.5,fill_color=YELLOW,).move_to(pricesAx.coords_to_point(i+0.5,0.2+(price-0.2)/2))
            rect.set_z_index(-1)
            pricesAx.add(rect)
    
        yax=pricesAx.get_y_axis()
        xax=pricesAx.get_x_axis()
        yax.shift(xax.width*RIGHT)
        pricesAx.add(pricesAx.get_y_axis_label(Tex("Prices",color=YELLOW).scale(0.2).rotate(-90*DEGREES),direction=RIGHT,edge=RIGHT))
        timelbl = axes.get_x_axis_label(Tex("Time",color=WHITE).scale(0.2),direction=0.8*DOWN,edge=DOWN)
        pricesAx.add(timelbl)
        self.play(ReplacementTransform(midLPCopy,pricesAx))
        self.wait(1)

        # Shift y axis
        xax = axes.get_x_axis()
        yax = axes.get_y_axis()
        #yax.shift(xax.width*RIGHT)
        yax.set_z_index(0)
        axes.add(axes.get_y_axis_label(Tex("Power",color=BLUE).scale(0.2).rotate(90*DEGREES),direction=LEFT,edge=LEFT))

        self.play(Create(axes))
        scale = 5 / axes.bars[0].height

        #Objective value
        objVal = DecimalNumber(0,font_size=30,).scale(0.5).next_to(frameSolver,0.7*UP)
        objLbl = Text("Objective value:",font="Satoshi",font_size=30).scale(0.4).next_to(objVal,LEFT)
        objVal.add_updater(lambda d: d.set_value(scale*np.sum(np.array([bar.height for bar in axes.bars])*np.array(prices))))
        objVal.add_updater(lambda d: d.next_to(objLbl,RIGHT))

        self.play(Write(objLbl),Write(objVal),run_time=0.5)

        self.play(axes.animate.change_bar_values([3,6,7,3,6,6,7,4,6,2]),run_time=0.6)
        self.play(axes.animate.change_bar_values([8,10,3,5,2,5,2,9,2,4]),run_time=0.6)
        self.play(axes.animate.change_bar_values([0,0,0,0,10,10,10,10,10,0]),run_time=0.6)

        self.wait(1)
        self.play(Indicate(objVal,color=GREEN))
        pricesAx.remove(timelbl)
        axes.add(timelbl)
        self.add(axes)
        self.play(FadeOut(objLbl),FadeOut(objVal),FadeOut(pricesAx),FadeOut(frameSolver))
        arrrow = Arrow(solver.get_right(),solver.get_right()+0.5*RIGHT,buff=0.1)
        self.play(axes.animate.scale(0.5).next_to(solver,1.8*RIGHT),GrowArrow(arrrow))

        self.wait(0.5)
        self.play(Restore(self.camera.frame))
        self.wait(1)

        # Reset
        self.play(*[FadeOut(mob) for mob in self.mobjects[1:]])


class Conclusion(Scene):

    def construct(self):
        
        # Add the assistant
        robotSVG.scale(0.25).to_edge(UP)
        self.add(robotSVG)
        self.play(robotSVG.animate.center().scale(3))

        # Title
        title = Text("Demo using OpenAI API",font="Satoshi",font_size=50).center()

        self.play(ReplacementTransform(robotSVG,title))
        self.wait(2)
        self.play(FadeOut(title))

class CommentLP(Scene):
    def construct(self):
        # Show image full screen
        comment = ImageMobject("/home/thomasmong/Videos/demo/last-frame.png",scale_to_resolution=2160)
        self.add(comment)
        self.wait(1)

        # Indicate request param
        rect = Rectangle(height=0.18,width=0.5,stroke_width=3,color=RED).shift(5.91*LEFT+2.93*UP)
        self.play(Create(rect))
        self.play(Indicate(rect,color=RED))
        
        # Indicate time
        rectStart = Rectangle(height=0.15,width=0.53,stroke_width=3,color=RED).shift(1.049*RIGHT+0.099*DOWN)
        rectStop = Rectangle(height=0.15,width=0.53,stroke_width=3,color=RED).shift(3.049*RIGHT+0.099*DOWN)
        self.play(ReplacementTransform(rect.copy(),rectStart),ReplacementTransform(rect.copy(),rectStop))
        self.play(Indicate(rectStart,color=RED),Indicate(rectStop,color=RED))
        self.wait(1)

        # Fade out
        self.play(FadeOut(rect),FadeOut(rectStart),FadeOut(rectStop))

        # Line sync
        gr = VGroup()
        top = 2.46*UP
        bot = 2.88*DOWN
        pad = 0.1113
        start = 0.936
        colors = [RED,GREEN,PURPLE,ORANGE,LIGHT_BROWN,BLUE_D]
        ordd = [start-pad,start,start+3*pad,start+4*pad,start+5*pad,start+6*pad, start+7*pad, start+8*pad, start+10*pad, start+16*pad, start+17*pad, start+19*pad]
        for i,el in enumerate(ordd):
            line = Line(start=el*RIGHT+top,end=el*RIGHT+bot,stroke_width=2,color=colors[i//2])
            gr += line
            if i%2 == 1:
                self.play(Create(gr),run_time=0.8)
                self.wait(0.5)
                self.play(FadeOut(gr),run_time=0.5)
                gr = VGroup()
        #self.play(Create(gr))
        self.wait(1)
        

"""
class CommentMM(Scene):
    def construct(self):
        # Show image full screen
        comment = ImageMobject("/home/thomasmong/Videos/demo-MM/last-frame.png",scale_to_resolution=2160)
        self.add(comment)
        self.wait(3)

        # Indicate request param
        rect = Rectangle(height=0.18,width=0.5,stroke_width=3,color=RED).shift(5.255*LEFT+2.93*UP)
        self.play(Create(rect))
        self.play(Indicate(rect,color=RED))
        
        # Indicate time
        rectStart = Rectangle(height=0.15,width=0.53,stroke_width=3,color=RED).shift(0.824*RIGHT+1.18*UP)
        rectStop = Rectangle(height=0.15,width=0.53,stroke_width=3,color=RED).shift(6.052*RIGHT+1.18*UP)
        self.play(ReplacementTransform(rect.copy(),rectStart),ReplacementTransform(rect.copy(),rectStop))
        self.play(Indicate(rectStart,color=RED),Indicate(rectStop,color=RED))
        self.wait(4)
"""

class Credits(Scene):
    def construct(self):
        # Title
        title = Text("Credits",font="Satoshi",font_size=40).center().shift(2*UP)
        self.play(Write(title))
        self.wait(0.2)

        # Text
        writing = Text("Writing: Thomas Mongaillard and Samson Lasaulce",font="Satoshi",font_size=50).scale(0.3).next_to(title,4*DOWN)
        animation = Text("Animation: Thomas Mongaillard",font="Satoshi",font_size=50).scale(0.3).next_to(writing,DOWN)
        music = Text("Music: Sergii Pavkin from Pixabay",font="Satoshi",font_size=50).scale(0.3).next_to(animation,DOWN)
        self.play(FadeIn(writing))
        self.play(FadeIn(animation))
        self.play(FadeIn(music))
        self.wait(1)
        self.play(FadeOut(title),FadeOut(writing),FadeOut(animation),FadeOut(music))