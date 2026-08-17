from manim import *
import numpy as np

BG        = "#1a1a2e"
ACCENT    = "#e94560"
GOLD      = "#f5c542"
TEAL      = "#16c79a"
SOFT_BLUE = "#7ec8e3"
PINK      = "#ff6b9d"
CAP_COL   = YELLOW


def cap(text, **kw):
    kw.setdefault("font_size", 22)
    kw.setdefault("color", CAP_COL)
    kw.setdefault("line_spacing", 1.05)
    t = Text(text, **kw)
    t.to_edge(DOWN, buff=0.3)
    return t


class MDPVideo(Scene):

    def build_mdp(self):
        self.S = {
            "x0":  np.array([-5.2,  0,   0]),
            "x1L": np.array([-2.0,  1.9, 0]),
            "x2L": np.array([-2.0, -1.9, 0]),
            "x1R": np.array([ 1.6,  1.9, 0]),
            "x2R": np.array([ 1.6, -1.9, 0]),
            "T":   np.array([ 4.8,  0,   0]),
        }
        R = 0.52; self.state_radius = R
        colors = {"x0":WHITE,"x1L":GREEN_C,"x2L":GREEN_C,
                  "x1R":ORANGE,"x2R":ORANGE,"T":BLUE_C}
        nice = {"x0":"x_0","x1L":"x_1^L","x2L":"x_2^L",
                "x1R":"x_1^R","x2R":"x_2^R","T":"x_H"}
        self.nice = nice
        self.state_data = {
            "x0":  (0.2, 0.8, [0.9,0.1], [0.8,0.2]),
            "x1L": (0.3, 0.4, [0.4,0.6], [0.5,0.5]),
            "x2L": (0.5, 0.6, [0.1,0.9], [0.3,0.7]),
            "x1R": (0.3, 0.4, [1],[1]),
            "x2R": (0.7, 0.8, [1],[1]),
        }
        self.circles={}; self.labels={}; self.act_dots={}; self.info_txts={}
        self.mdp_group = VGroup()
        for k in ["x0","x1L","x2L","x1R","x2R","T"]:
            c = Circle(radius=R, color=colors[k], stroke_width=2.5).move_to(self.S[k])
            self.circles[k]=c
            l = MathTex(nice[k], font_size=22, color=colors[k]).next_to(c, DOWN, buff=0.12)
            self.labels[k]=l; self.mdp_group.add(c,l)
            if k in self.state_data:
                r1,r2,t1,t2 = self.state_data[k]
                d1=Dot(self.S[k]+UP*0.2, radius=0.05, color=WHITE)
                d2=Dot(self.S[k]+DOWN*0.2, radius=0.05, color=WHITE)
                self.act_dots[k]=(d1,d2)
                i1=Text(f"{r1}  {str(t1).replace(' ','')}", font_size=11, color=GREY_B)
                i1.next_to(d1, RIGHT, buff=0.06)
                i2=Text(f"{r2}  {str(t2).replace(' ','')}", font_size=11, color=GREY_B)
                i2.next_to(d2, RIGHT, buff=0.06)
                self.info_txts[k]=(i1,i2); self.mdp_group.add(d1,d2,i1,i2)
        self.layer_labs = VGroup(
            Text("Layer 0",font_size=14,color=GREY).move_to([-5.2,-2.8,0]),
            Text("Layer 1",font_size=14,color=GREY).move_to([-2.0,-2.8,0]),
            Text("Layer 2",font_size=14,color=GREY).move_to([ 1.6,-2.8,0]),
            Text("Terminal",font_size=14,color=GREY).move_to([ 4.8,-2.8,0]),
        )
        self.mdp_group.add(self.layer_labs)
        self.trans_arrows = VGroup()
        for src,dsts in [("x0",["x1L","x2L"]),("x1L",["x1R","x2R"]),
                         ("x2L",["x1R","x2R"]),("x1R",["T"]),("x2R",["T"])]:
            for dst in dsts:
                a = Arrow(self.S[src],self.S[dst],buff=R+0.08,stroke_width=1.2,
                          color=GREY_C,max_tip_length_to_length_ratio=0.08)
                self.trans_arrows.add(a)
        self.mdp_group.add(self.trans_arrows)

    def hl(self, key, color=ACCENT):
        return SurroundingRectangle(self.circles[key], color=color,
                                     buff=0.08, stroke_width=2.5, corner_radius=0.3)

    def fade_mdp(self, op=0.12):
        self.play(*[m.animate.set_opacity(op) for m in self.mdp_group], run_time=0.6)

    def restore_mdp(self):
        self.play(*[m.animate.set_opacity(1.0) for m in self.mdp_group], run_time=0.6)

    def make_agent(self):
        a = Triangle(color=ACCENT, fill_opacity=0.9).scale(0.16)
        l = Text("Agent", font_size=13, color=ACCENT).next_to(a, UP, buff=0.06)
        return VGroup(a, l)

    def flash_reward(self, ag, rew, rt=0.3):
        r = Text(f"+{rew}", font_size=20, color=GOLD)
        r.next_to(ag, RIGHT, buff=0.1)
        self.play(FadeIn(r, shift=UP*0.08), run_time=rt)
        self.wait(0.25)
        self.play(FadeOut(r), run_time=0.2)

    # ──────────────────────────────────────────
    def construct(self):
        self.camera.background_color = BG
        self.build_mdp()

        # ═══════════════════ TITLE ═══════════════════
        title = Text("Markov Decision\nProcesses", font_size=52,
                      color=WHITE, line_spacing=1.2)
        tag = Text("(MDPs)", font_size=32, color=SOFT_BLUE).next_to(title, DOWN, buff=0.4)
        self.play(Write(title, run_time=1.5))
        self.play(FadeIn(tag, shift=UP*0.2))
        self.wait(1.5)
        self.play(FadeOut(title), FadeOut(tag)); self.wait(0.3)

        # ═══════════════════ PART 1 – BUILD MDP ═══════════════════
        c = cap("An MDP generalizes the\nbandit problem to\nmultiple states.")
        self.play(FadeIn(c))
        self.play(LaggedStart(*[FadeIn(m) for m in self.mdp_group],
                               lag_ratio=0.02), run_time=2)
        self.wait(1)

        c2 = cap("Each circle is a state.")
        self.play(FadeTransform(c, c2))
        shl = VGroup(*[SurroundingRectangle(self.circles[k], color=TEAL,
              buff=0.06, stroke_width=2, corner_radius=0.3)
              for k in ["x0","x1L","x2L","x1R","x2R","T"]])
        self.play(Create(shl), run_time=0.8); self.wait(1.5)
        self.play(FadeOut(shl))

        c3 = cap("Dots inside are\navailable actions.")
        self.play(FadeTransform(c2, c3))
        dhl = VGroup()
        for k in self.act_dots:
            for d in self.act_dots[k]:
                dhl.add(Circle(radius=0.1, color=PINK, stroke_width=2.5).move_to(d))
        self.play(Create(dhl), run_time=0.8)
        a1l = Text("a₁ (top)", font_size=16, color=PINK).next_to(self.act_dots["x0"][0], LEFT, buff=0.45)
        a2l = Text("a₂ (bottom)", font_size=16, color=PINK).next_to(self.act_dots["x0"][1], LEFT, buff=0.45)
        self.play(FadeIn(a1l), FadeIn(a2l)); self.wait(2)
        self.play(FadeOut(dhl), FadeOut(a1l), FadeOut(a2l))

        c4 = cap("Number next to the dot\nis the immediate reward.\nBrackets are transition\nprobabilities.")
        self.play(FadeTransform(c3, c4)); self.wait(3)

        c5 = cap("States are in layers.\nEach step moves you\none layer forward.")
        self.play(FadeTransform(c4, c5))
        self.play(*[ll.animate.set_color(GOLD) for ll in self.layer_labs], run_time=0.5)
        self.wait(2)
        self.play(*[ll.animate.set_color(GREY) for ll in self.layer_labs], run_time=0.3)
        self.play(FadeOut(c5))

        # ═══════════════════ PART 2 – POLICY + TRAVERSALS ═══════════════════
        c = cap("A policy π maps each\nstate to an action.")
        self.play(FadeIn(c))
        peq = MathTex(r"\pi : \mathcal{S} \to \mathcal{A}", font_size=32, color=TEAL)
        peq.to_edge(UP, buff=0.4)
        self.play(Write(peq)); self.wait(1.5)
        c2 = cap("Example policy:\nchoose a₂ everywhere.")
        self.play(FadeTransform(c, c2))
        ptable = MathTex(
            r"\pi(x_0)\!=\!a_2,\;"
            r"\pi(x_1^L)\!=\!a_2,\;"
            r"\pi(x_2^L)\!=\!a_2,\;"
            r"\pi(x_1^R)\!=\!a_2,\;"
            r"\pi(x_2^R)\!=\!a_2",
            font_size=18, color=TEAL)
        ptable.next_to(peq, DOWN, buff=0.25)
        self.play(Write(ptable), run_time=1.2)
        phl = VGroup(*[Circle(radius=0.11, color=TEAL, stroke_width=3).move_to(
            self.act_dots[k][1]) for k in ["x0","x1L","x2L","x1R","x2R"]])
        self.play(Create(phl), run_time=0.8); self.wait(2.5)
        self.play(FadeOut(phl), FadeOut(peq), FadeOut(ptable), FadeOut(c2))

        # traversals
        c = cap("Let's run this policy\nfor several iterations.")
        self.play(FadeIn(c))

        pol_display = VGroup(
            Text("Policy π", font_size=14, color=TEAL),
            MathTex(r"\pi(\cdot)=a_2\;\forall\,x", font_size=16, color=TEAL)
        ).arrange(DOWN, buff=0.06)
        pol_bg = SurroundingRectangle(pol_display, color=TEAL, buff=0.1,
                                       stroke_width=1.5, fill_color=BG, fill_opacity=0.85)
        pol_grp = VGroup(pol_bg, pol_display).to_corner(UR, buff=0.3)
        self.play(FadeIn(pol_grp))

        ag = self.make_agent()
        ag.move_to(self.S["x0"]+UP*(self.state_radius+0.22))
        self.play(FadeIn(ag, shift=DOWN*0.2)); self.wait(0.3)
        self.play(FadeOut(c))

        trajs = [
            ("Iter 1",[("x0",1,0.8,"x1L"),("x1L",1,0.4,"x1R"),("x1R",1,0.4,"T")],1.6),
            ("Iter 2",[("x0",1,0.8,"x1L"),("x1L",1,0.4,"x2R"),("x2R",1,0.8,"T")],2.0),
            ("Iter 3",[("x0",1,0.8,"x2L"),("x2L",1,0.6,"x2R"),("x2R",1,0.8,"T")],2.2),
        ]
        results = VGroup()
        for ti,(label,traj,_) in enumerate(trajs):
            ag.move_to(self.S["x0"]+UP*(self.state_radius+0.22))
            cnt = Text(f"{label}  reward: 0.0", font_size=18, color=GOLD)
            cnt.to_edge(UP, buff=0.35+ti*0.35).to_edge(LEFT, buff=0.3)
            self.play(FadeIn(cnt), run_time=0.3)
            total = 0.0
            for sk,ai,rew,nsk in traj:
                chosen = self.act_dots[sk][ai]
                hlc = Circle(radius=0.09, color=ACCENT, stroke_width=3).move_to(chosen)
                self.play(Create(hlc), run_time=0.25)
                self.flash_reward(ag, rew)
                total += rew
                nc = Text(f"{label}  reward: {total:.1f}", font_size=18, color=GOLD).move_to(cnt)
                self.play(FadeTransform(cnt, nc), run_time=0.2); cnt=nc
                self.play(ag.animate.move_to(self.S[nsk]+UP*(self.state_radius+0.22)),
                          FadeOut(hlc), run_time=0.45)
            final = Text(f"{label}: total = {total:.1f}", font_size=18, color=GOLD).move_to(cnt)
            self.play(FadeTransform(cnt, final), run_time=0.25)
            results.add(final); self.wait(0.2)

        avg = (1.6+2.0+2.2)/3
        avt = Text(f"Average ≈ {avg:.2f}", font_size=20, color=ACCENT)
        avt.next_to(results, DOWN, buff=0.2, aligned_edge=LEFT)
        self.play(FadeIn(avt))
        cs = cap("Same policy, different\noutcomes each time!")
        self.play(FadeIn(cs)); self.wait(2.5)
        self.play(FadeOut(results), FadeOut(avt), FadeOut(ag),
                  FadeOut(cs), FadeOut(pol_grp))

        # ═══════════════════════════════════════════════════════════
        #  PART 3 – V VALUE (equation + brief visual, no zoom)
        # ═══════════════════════════════════════════════════════════
        vt = Text("V-Value Function", font_size=36, color=TEAL).to_edge(UP, buff=0.4)
        self.fade_mdp()
        self.play(FadeIn(vt))

        c = cap("V is the expected total\nreward from a state,\nfollowing policy π.")
        self.play(FadeIn(c)); self.wait(2.5)

        v_eq = MathTex(
            r"V_h^\pi(x)", r"=", r"\mathbb{E}",
            r"\!\left[\sum_{h'=h}^{H} r_{h'}\!\bigl(x_{h'},\pi(x_{h'})\bigr)\right]",
            font_size=30, color=WHITE).move_to(ORIGIN+UP*0.3)
        self.play(Write(v_eq), run_time=1.5); self.wait(1)

        c2 = cap("h is your current layer.\nThe sum collects rewards\nfrom h to the end.")
        self.play(FadeTransform(c, c2))
        brace = Brace(v_eq[3], DOWN, color=GREY_B)
        blab = Text("sum of rewards\nfollowing π", font_size=16,
                     color=GREY_B, line_spacing=1.0).next_to(brace, DOWN, buff=0.1)
        self.play(Create(brace), FadeIn(blab)); self.wait(2.5)

        c3 = cap("The expectation is over\nrandom transitions.")
        self.play(FadeTransform(c2, c3))
        ehl = SurroundingRectangle(v_eq[2], color=SOFT_BLUE, buff=0.06, stroke_width=2)
        self.play(Create(ehl)); self.wait(2.5)
        self.play(FadeOut(brace), FadeOut(blab), FadeOut(ehl),
                  FadeOut(v_eq), FadeOut(vt), FadeOut(c3))

        # ═══════════════════════════════════════════════════════════
        #  PART 4 – Q VALUE (equation + brief, no zoom)
        # ═══════════════════════════════════════════════════════════
        qt = Text("Q-Value Function", font_size=36, color=PINK).to_edge(UP, buff=0.4)
        self.play(FadeIn(qt))

        c = cap("Q is the expected total\nif you take action a\nfirst, then follow π.")
        self.play(FadeIn(c)); self.wait(2.5)

        q_eq = MathTex(
            r"Q_h^\pi(x,a)", r"=", r"r_h(x,a)",
            r"+\;\mathbb{E}\!\left[\sum_{h'=h+1}^{H}"
            r"r_{h'}\!\bigl(x_{h'},\pi(x_{h'})\bigr)\right]",
            font_size=28, color=WHITE).move_to(ORIGIN+UP*0.3)
        self.play(Write(q_eq), run_time=1.5); self.wait(1)

        c2 = cap("First term: immediate\nreward of your action.")
        self.play(FadeTransform(c, c2))
        br_r = Brace(q_eq[2], DOWN, color=GOLD)
        br_rl = Text("immediate reward", font_size=15, color=GOLD).next_to(br_r, DOWN, buff=0.08)
        self.play(Create(br_r), FadeIn(br_rl)); self.wait(2)

        c3 = cap("Second term: expected\nfuture following π.")
        self.play(FadeTransform(c2, c3))
        br_f = Brace(q_eq[3], DOWN, color=SOFT_BLUE)
        br_fl = Text("future following π", font_size=15, color=SOFT_BLUE).next_to(br_f, DOWN, buff=0.08)
        self.play(Create(br_f), FadeIn(br_fl)); self.wait(2)
        self.play(FadeOut(br_r), FadeOut(br_rl), FadeOut(br_f), FadeOut(br_fl))

        c4 = cap("V picks the Q of the\naction π chooses.")
        self.play(FadeTransform(c3, c4))
        vq = MathTex(r"V_h^\pi(x)=Q_h^\pi(x,\,\pi(x))",
                     font_size=28, color=GOLD).move_to(ORIGIN+DOWN*1.2)
        self.play(Write(vq)); self.wait(2.5)
        self.play(FadeOut(q_eq), FadeOut(vq), FadeOut(qt), FadeOut(c4))

        # ═══════════════════════════════════════════════════════════
        #  PART 5 – BELLMAN EQUATIONS + RECURSION DIAGRAM
        # ═══════════════════════════════════════════════════════════
        bt = Text("Bellman Equations", font_size=36, color=GOLD).to_edge(UP, buff=0.4)
        self.play(FadeIn(bt))

        c = cap("We can compute V and Q\nwith a recursion instead\nof simulating.")
        self.play(FadeIn(c)); self.wait(2.5)

        c2 = cap("For the optimal policy:")
        self.play(FadeTransform(c, c2))

        oq = MathTex(
            r"Q_h^\star(x,a) = r_h(x,a) + "
            r"\sum_{x'} P(x'\!\mid\! x,a)\,V_{h+1}^\star(x')",
            font_size=26, color=WHITE).move_to(UP*0.8)
        ov = MathTex(
            r"V_h^\star(x) = \max_{a}\; Q_h^\star(x,a)",
            font_size=26, color=GOLD).move_to(DOWN*0.2)
        self.play(Write(oq), run_time=1.2)
        self.play(Write(ov), run_time=0.8); self.wait(1.5)

        c3 = cap("V takes the max Q:\npick the best action.")
        self.play(FadeTransform(c2, c3))
        max_hl = SurroundingRectangle(ov[0][7:13], color=ACCENT, buff=0.06, stroke_width=3)
        self.play(Create(max_hl)); self.wait(2.5)

        # ── Recursion diagram ──
        c4 = cap("Why does the Q recursion\nwork? Let's see.")
        self.play(FadeTransform(c3, c4), FadeOut(max_hl),
                  oq.animate.set_opacity(0.15), ov.animate.set_opacity(0.15),
                  FadeOut(bt))

        dx = Circle(radius=0.45, color=WHITE, stroke_width=2.5).move_to(LEFT*4)
        dx_lab = MathTex(r"x", font_size=24, color=WHITE).move_to(dx)
        dx_dot = Dot(dx.get_center()+DOWN*0.15, radius=0.05, color=GOLD)
        dx_a = MathTex(r"a", font_size=18, color=GOLD).next_to(dx_dot, LEFT, buff=0.1)

        ns = [UP*1.5, ORIGIN, DOWN*1.5]
        ns_circs = VGroup()
        ns_labs = VGroup()
        ns_vs = VGroup()
        ns_arrows = VGroup()
        ns_plabs = VGroup()
        for i, ny in enumerate(ns):
            nc = Circle(radius=0.4, color=SOFT_BLUE, stroke_width=2).move_to(RIGHT*1+ny)
            ns_circs.add(nc)
            nl = MathTex(f"x'_{i+1}", font_size=18, color=SOFT_BLUE).move_to(nc)
            ns_labs.add(nl)
            vl = MathTex(f"V(x'_{i+1})", font_size=16, color=GOLD).next_to(nc, RIGHT, buff=0.15)
            ns_vs.add(vl)
            arr = Arrow(dx.get_right(), nc.get_left(), buff=0.08, stroke_width=1.5,
                        color=GREY_B, max_tip_length_to_length_ratio=0.1)
            ns_arrows.add(arr)
            pl = MathTex(f"P_{i+1}", font_size=14, color=PINK)
            pl.next_to(arr, UP if i==0 else (UP if i==1 else DOWN), buff=0.05)
            ns_plabs.add(pl)

        diag = VGroup(dx, dx_lab, dx_dot, dx_a, ns_circs, ns_labs,
                      ns_vs, ns_arrows, ns_plabs)
        diag.move_to(LEFT*1.5+UP*0.3)

        self.play(FadeIn(dx), FadeIn(dx_lab)); self.wait(0.3)

        c5 = cap("You take action a and\nget reward r(x,a).")
        self.play(FadeTransform(c4, c5))
        self.play(FadeIn(dx_dot), FadeIn(dx_a))
        rew_lbl = MathTex(r"r(x,a)", font_size=20, color=GOLD).next_to(dx, UP, buff=0.2)
        self.play(FadeIn(rew_lbl)); self.wait(2)

        c6 = cap("Then you land in one of\nthe next-layer states.")
        self.play(FadeTransform(c5, c6))
        self.play(LaggedStart(*[FadeIn(nc) for nc in ns_circs], lag_ratio=0.15),
                  LaggedStart(*[FadeIn(nl) for nl in ns_labs], lag_ratio=0.15),
                  LaggedStart(*[Create(a) for a in ns_arrows], lag_ratio=0.15), run_time=1)
        self.play(LaggedStart(*[FadeIn(p) for p in ns_plabs], lag_ratio=0.15), run_time=0.6)
        self.wait(2)

        c7 = cap("From each next state,\nV gives the expected\nfuture reward\nby definition.")
        self.play(FadeTransform(c6, c7))
        self.play(LaggedStart(*[FadeIn(v) for v in ns_vs], lag_ratio=0.15), run_time=0.8)
        self.wait(2.5)

        c8 = cap("Weight each V by the\nprobability of landing\nthere. Add the reward.")
        self.play(FadeTransform(c7, c8))
        q_build = MathTex(
            r"Q(x,a)=",
            r"\underbrace{r(x,a)}_{\text{reward}}",
            r"+\underbrace{P_1 V(x'_1)+P_2 V(x'_2)+P_3 V(x'_3)}_{\text{weighted future}}",
            font_size=18, color=WHITE).move_to(DOWN*2.5)
        self.play(Write(q_build), run_time=1.5); self.wait(3)

        self.play(FadeOut(diag), FadeOut(rew_lbl), FadeOut(q_build), FadeOut(c8))
        c9 = cap("We solve this from the\nlast layer backward.")
        self.play(FadeIn(c9)); self.wait(2)
        self.play(FadeOut(c9))

        # ═══════════════════════════════════════════════════════════
        #  PART 6 – BACKWARD INDUCTION
        # ═══════════════════════════════════════════════════════════
        self.restore_mdp()

        # Pin Bellman equations in top-left as reference
        bell_ref = VGroup(
            MathTex(r"Q_h^\star(x,a)=r_h(x,a)+\sum_{x'}P(x'|x,a)\,V_{h+1}^\star(x')",
                    font_size=14, color=GREY_B),
            MathTex(r"V_h^\star(x)=\max_a Q_h^\star(x,a)",
                    font_size=14, color=GOLD_E),
        ).arrange(DOWN, buff=0.08, aligned_edge=LEFT)
        bell_bg = SurroundingRectangle(bell_ref, color=GREY, buff=0.1,
                                        stroke_width=1, fill_color=BG, fill_opacity=0.85,
                                        corner_radius=0.05)
        bell_pin = VGroup(bell_bg, bell_ref).to_corner(UL, buff=0.25)
        self.play(FadeOut(oq), FadeOut(ov), FadeIn(bell_pin), run_time=0.6)

        ex = Text("Example", font_size=20, color=ACCENT)
        ex.next_to(bell_pin, DOWN, buff=0.12, aligned_edge=LEFT)
        self.play(FadeIn(ex))
        SP_Y = 3.2

        # Initialize
        c = cap("Initialize: V at the\nterminal state is 0.")
        self.play(FadeIn(c))
        hl_t = self.hl("T", BLUE_C)
        self.play(Create(hl_t))
        v_T = MathTex(r"V^\star\!=\!0", font_size=14, color=GOLD)
        v_T.next_to(self.circles["T"], UP, buff=0.08)
        self.play(FadeIn(v_T)); self.wait(1.5)
        self.play(FadeOut(hl_t))

        # ── Layer 2: x1R (show Q = r + 1·0) ──
        c2 = cap("Layer 2: solve x₁ᴿ.\nActions go to terminal.")
        self.play(FadeTransform(c, c2))
        hl = self.hl("x1R"); self.play(Create(hl))

        eq1 = MathTex(r"Q^\star(x_1^R,a_1)",r"=",r"0.3",r"+\,1",r"\!\cdot\!0",r"=0.3",
                      font_size=17, color=WHITE).move_to([4.0, SP_Y, 0])
        self.play(FadeIn(eq1[0]),FadeIn(eq1[1]), run_time=0.5)
        self.play(Indicate(self.act_dots["x1R"][0], color=GOLD, scale_factor=2.0), run_time=0.7)
        self.play(FadeIn(eq1[2]), run_time=0.4)
        self.play(Indicate(self.info_txts["x1R"][0], color=GOLD, scale_factor=1.5), run_time=0.7)
        self.play(FadeIn(eq1[3]), run_time=0.3)
        self.play(Indicate(self.trans_arrows[6], color=SOFT_BLUE, scale_factor=1.2), run_time=0.6)
        self.play(FadeIn(eq1[4]), run_time=0.3)
        self.play(Indicate(v_T, color=GOLD, scale_factor=2.0), run_time=0.6)
        self.play(FadeIn(eq1[5]), run_time=0.4); self.wait(0.5)

        eq2 = MathTex(r"Q^\star(x_1^R,a_2)",r"=",r"0.4",r"+\,1",r"\!\cdot\!0",r"=0.4",
                      font_size=17, color=WHITE).next_to(eq1, DOWN, buff=0.12, aligned_edge=LEFT)
        self.play(FadeIn(eq2[0]),FadeIn(eq2[1]), run_time=0.4)
        self.play(Indicate(self.act_dots["x1R"][1], color=GOLD, scale_factor=2.0), run_time=0.6)
        self.play(FadeIn(eq2[2]), run_time=0.3)
        self.play(Indicate(self.info_txts["x1R"][1], color=GOLD, scale_factor=1.5), run_time=0.6)
        self.play(FadeIn(eq2[3]),FadeIn(eq2[4]),FadeIn(eq2[5]), run_time=0.4); self.wait(0.5)

        c2b = cap("Two Q values. Pick the\nlarger one for V*.")
        self.play(FadeTransform(c2, c2b))
        win = SurroundingRectangle(eq2, color=TEAL, buff=0.04, stroke_width=2)
        self.play(Create(win)); self.wait(1)
        spv = MathTex(r"V^\star(x_1^R)=\max\{0.3,0.4\}=0.4", font_size=17, color=GOLD)
        spv.next_to(eq2, DOWN, buff=0.15, aligned_edge=LEFT)
        self.play(Write(spv), run_time=0.8); self.wait(1)

        v1r = MathTex(r"V^\star\!=\!0.4", font_size=14, color=GOLD)
        v1r.next_to(self.circles["x1R"], UP, buff=0.08)
        self.play(FadeIn(v1r), FadeOut(eq1),FadeOut(eq2),FadeOut(spv),FadeOut(win),FadeOut(hl))

        # ── Layer 2: x2R ──
        c3 = cap("Layer 2: solve x₂ᴿ.")
        self.play(FadeTransform(c2b, c3))
        hl = self.hl("x2R"); self.play(Create(hl))
        eq1 = MathTex(r"Q^\star(x_2^R,a_1)",r"=",r"0.7",r"+\,1",r"\!\cdot\!0",r"=0.7",
                      font_size=17, color=WHITE).move_to([4.0, SP_Y, 0])
        self.play(FadeIn(eq1[0]),FadeIn(eq1[1]), run_time=0.4)
        self.play(Indicate(self.act_dots["x2R"][0], color=GOLD, scale_factor=2.0), run_time=0.6)
        self.play(FadeIn(eq1[2]), run_time=0.3)
        self.play(Indicate(self.info_txts["x2R"][0], color=GOLD, scale_factor=1.5), run_time=0.6)
        self.play(FadeIn(eq1[3]),FadeIn(eq1[4]),FadeIn(eq1[5]), run_time=0.4); self.wait(0.3)

        eq2 = MathTex(r"Q^\star(x_2^R,a_2)",r"=",r"0.8",r"+\,1",r"\!\cdot\!0",r"=0.8",
                      font_size=17, color=WHITE).next_to(eq1, DOWN, buff=0.12, aligned_edge=LEFT)
        self.play(FadeIn(eq2[0]),FadeIn(eq2[1]), run_time=0.3)
        self.play(Indicate(self.act_dots["x2R"][1], color=GOLD, scale_factor=2.0), run_time=0.5)
        self.play(FadeIn(eq2[2]), run_time=0.3)
        self.play(Indicate(self.info_txts["x2R"][1], color=GOLD, scale_factor=1.5), run_time=0.5)
        self.play(FadeIn(eq2[3]),FadeIn(eq2[4]),FadeIn(eq2[5]), run_time=0.4); self.wait(0.3)

        c3b = cap("Pick the larger Q.")
        self.play(FadeTransform(c3, c3b))
        win = SurroundingRectangle(eq2, color=TEAL, buff=0.04, stroke_width=2)
        self.play(Create(win)); self.wait(0.8)
        spv = MathTex(r"V^\star(x_2^R)=\max\{0.7,0.8\}=0.8", font_size=17, color=GOLD)
        spv.next_to(eq2, DOWN, buff=0.15, aligned_edge=LEFT)
        self.play(Write(spv), run_time=0.8); self.wait(1)
        v2r = MathTex(r"V^\star\!=\!0.8", font_size=14, color=GOLD)
        v2r.next_to(self.circles["x2R"], UP, buff=0.08)
        self.play(FadeIn(v2r), FadeOut(eq1),FadeOut(eq2),FadeOut(spv),FadeOut(win),FadeOut(hl))

        # ── Layer 1: x1L (longer beats) ──
        c4 = cap("Layer 1: solve x₁ᴸ.\nQ now uses the V values\nwe just found.")
        self.play(FadeTransform(c3b, c4))
        hl = self.hl("x1L"); self.play(Create(hl))

        eq1 = MathTex(r"Q^\star(x_1^L,a_1)",r"=",r"0.3",r"+\,0.4",r"\!\cdot\!0.4",
                      r"+\,0.6",r"\!\cdot\!0.8",r"=0.94",
                      font_size=16, color=WHITE).move_to([3.5, SP_Y, 0])
        self.play(FadeIn(eq1[0]),FadeIn(eq1[1]), run_time=0.5)
        self.play(Indicate(self.act_dots["x1L"][0], color=GOLD, scale_factor=2.0), run_time=0.7); self.wait(0.3)
        self.play(FadeIn(eq1[2]), run_time=0.5)
        self.play(Indicate(self.info_txts["x1L"][0], color=GOLD, scale_factor=1.5), run_time=0.7); self.wait(0.3)
        self.play(FadeIn(eq1[3]), run_time=0.5)
        self.play(Indicate(self.trans_arrows[2], color=SOFT_BLUE, scale_factor=1.3), run_time=0.7); self.wait(0.2)
        self.play(FadeIn(eq1[4]), run_time=0.5)
        self.play(Indicate(v1r, color=GOLD, scale_factor=2.0), run_time=0.7); self.wait(0.3)
        self.play(FadeIn(eq1[5]), run_time=0.5)
        self.play(Indicate(self.trans_arrows[3], color=PINK, scale_factor=1.3), run_time=0.7); self.wait(0.2)
        self.play(FadeIn(eq1[6]), run_time=0.5)
        self.play(Indicate(v2r, color=GOLD, scale_factor=2.0), run_time=0.7); self.wait(0.3)
        self.play(FadeIn(eq1[7]), run_time=0.5); self.wait(0.8)

        eq2 = MathTex(r"Q^\star(x_1^L,a_2)",r"=",r"0.4",r"+\,0.5",r"\!\cdot\!0.4",
                      r"+\,0.5",r"\!\cdot\!0.8",r"=1.0",
                      font_size=16, color=WHITE).next_to(eq1, DOWN, buff=0.15, aligned_edge=LEFT)
        self.play(FadeIn(eq2[0]),FadeIn(eq2[1]), run_time=0.4)
        self.play(Indicate(self.act_dots["x1L"][1], color=GOLD, scale_factor=2.0), run_time=0.6)
        self.play(FadeIn(eq2[2]), run_time=0.4)
        self.play(Indicate(self.info_txts["x1L"][1], color=GOLD, scale_factor=1.5), run_time=0.6)
        self.play(FadeIn(eq2[3]), run_time=0.4)
        self.play(Indicate(self.trans_arrows[2], color=SOFT_BLUE, scale_factor=1.3), run_time=0.6)
        self.play(FadeIn(eq2[4]), run_time=0.4)
        self.play(Indicate(v1r, color=GOLD, scale_factor=2.0), run_time=0.6)
        self.play(FadeIn(eq2[5]), run_time=0.4)
        self.play(Indicate(self.trans_arrows[3], color=PINK, scale_factor=1.3), run_time=0.6)
        self.play(FadeIn(eq2[6]), run_time=0.4)
        self.play(Indicate(v2r, color=GOLD, scale_factor=2.0), run_time=0.6)
        self.play(FadeIn(eq2[7]), run_time=0.4); self.wait(0.8)

        c4b = cap("Two Q values: 0.94 and\n1.0. Pick the larger.")
        self.play(FadeTransform(c4, c4b))
        win = SurroundingRectangle(eq2, color=TEAL, buff=0.04, stroke_width=2)
        self.play(Create(win)); self.wait(1)
        spv = MathTex(r"V^\star(x_1^L)=\max\{0.94,1.0\}=1.0\;\;(a_2)", font_size=16, color=GOLD)
        spv.next_to(eq2, DOWN, buff=0.15, aligned_edge=LEFT)
        self.play(Write(spv), run_time=0.8); self.wait(1)
        v1l = MathTex(r"V^\star\!=\!1.0", font_size=14, color=GOLD)
        v1l.next_to(self.circles["x1L"], UP, buff=0.08)
        self.play(FadeIn(v1l), FadeOut(eq1),FadeOut(eq2),FadeOut(spv),FadeOut(win),FadeOut(hl))

        # ── Layer 1: x2L ──
        c5 = cap("Layer 1: solve x₂ᴸ.")
        self.play(FadeTransform(c4b, c5))
        hl = self.hl("x2L"); self.play(Create(hl))
        eq1 = MathTex(r"Q^\star(x_2^L,a_1)",r"=",r"0.5",r"+\,0.1",r"\!\cdot\!0.4",
                      r"+\,0.9",r"\!\cdot\!0.8",r"=1.26",
                      font_size=16, color=WHITE).move_to([3.5, SP_Y, 0])
        self.play(FadeIn(eq1[0]),FadeIn(eq1[1]), run_time=0.4)
        self.play(Indicate(self.act_dots["x2L"][0], color=GOLD, scale_factor=2.0), run_time=0.6)
        self.play(FadeIn(eq1[2]), run_time=0.4)
        self.play(Indicate(self.info_txts["x2L"][0], color=GOLD, scale_factor=1.5), run_time=0.6)
        self.play(FadeIn(eq1[3]), run_time=0.4)
        self.play(Indicate(self.trans_arrows[4], color=SOFT_BLUE, scale_factor=1.3), run_time=0.6)
        self.play(FadeIn(eq1[4]), run_time=0.4)
        self.play(Indicate(v1r, color=GOLD, scale_factor=2.0), run_time=0.6)
        self.play(FadeIn(eq1[5]), run_time=0.4)
        self.play(Indicate(self.trans_arrows[5], color=PINK, scale_factor=1.3), run_time=0.6)
        self.play(FadeIn(eq1[6]), run_time=0.4)
        self.play(Indicate(v2r, color=GOLD, scale_factor=2.0), run_time=0.6)
        self.play(FadeIn(eq1[7]), run_time=0.4); self.wait(0.5)

        eq2 = MathTex(r"Q^\star(x_2^L,a_2)",r"=",r"0.6",r"+\,0.3",r"\!\cdot\!0.4",
                      r"+\,0.7",r"\!\cdot\!0.8",r"=1.28",
                      font_size=16, color=WHITE).next_to(eq1, DOWN, buff=0.15, aligned_edge=LEFT)
        self.play(FadeIn(eq2[0]),FadeIn(eq2[1]), run_time=0.3)
        self.play(Indicate(self.act_dots["x2L"][1], color=GOLD, scale_factor=2.0), run_time=0.5)
        self.play(FadeIn(eq2[2]), run_time=0.3)
        self.play(Indicate(self.info_txts["x2L"][1], color=GOLD, scale_factor=1.5), run_time=0.5)
        self.play(FadeIn(eq2[3]), run_time=0.3)
        self.play(Indicate(self.trans_arrows[4], color=SOFT_BLUE, scale_factor=1.3), run_time=0.5)
        self.play(FadeIn(eq2[4]), run_time=0.3)
        self.play(Indicate(v1r, color=GOLD, scale_factor=2.0), run_time=0.5)
        self.play(FadeIn(eq2[5]), run_time=0.3)
        self.play(Indicate(self.trans_arrows[5], color=PINK, scale_factor=1.3), run_time=0.5)
        self.play(FadeIn(eq2[6]), run_time=0.3)
        self.play(Indicate(v2r, color=GOLD, scale_factor=2.0), run_time=0.5)
        self.play(FadeIn(eq2[7]), run_time=0.3); self.wait(0.5)

        c5b = cap("Pick the larger Q.")
        self.play(FadeTransform(c5, c5b))
        win = SurroundingRectangle(eq2, color=TEAL, buff=0.04, stroke_width=2)
        self.play(Create(win)); self.wait(0.8)
        spv = MathTex(r"V^\star(x_2^L)=\max\{1.26,1.28\}=1.28\;\;(a_2)", font_size=16, color=GOLD)
        spv.next_to(eq2, DOWN, buff=0.15, aligned_edge=LEFT)
        self.play(Write(spv), run_time=0.8); self.wait(1)
        v2l = MathTex(r"V^\star\!=\!1.28", font_size=14, color=GOLD)
        v2l.next_to(self.circles["x2L"], UP, buff=0.08)
        self.play(FadeIn(v2l), FadeOut(eq1),FadeOut(eq2),FadeOut(spv),FadeOut(win),FadeOut(hl))

        # ── Layer 0: x0 ──
        c6 = cap("Layer 0: solve x₀.")
        self.play(FadeTransform(c5b, c6))
        hl = self.hl("x0"); self.play(Create(hl))
        eq1 = MathTex(r"Q^\star(x_0,a_1)",r"=",r"0.2",r"+\,0.9",r"\!\cdot\!1.0",
                      r"+\,0.1",r"\!\cdot\!1.28",r"=1.228",
                      font_size=16, color=WHITE).move_to([3.5, SP_Y, 0])
        self.play(FadeIn(eq1[0]),FadeIn(eq1[1]), run_time=0.4)
        self.play(Indicate(self.act_dots["x0"][0], color=GOLD, scale_factor=2.0), run_time=0.6)
        self.play(FadeIn(eq1[2]), run_time=0.4)
        self.play(Indicate(self.info_txts["x0"][0], color=GOLD, scale_factor=1.5), run_time=0.6)
        self.play(FadeIn(eq1[3]), run_time=0.4)
        self.play(Indicate(self.trans_arrows[0], color=SOFT_BLUE, scale_factor=1.3), run_time=0.6)
        self.play(FadeIn(eq1[4]), run_time=0.4)
        self.play(Indicate(v1l, color=GOLD, scale_factor=2.0), run_time=0.6); self.wait(0.2)
        self.play(FadeIn(eq1[5]), run_time=0.4)
        self.play(Indicate(self.trans_arrows[1], color=PINK, scale_factor=1.3), run_time=0.6)
        self.play(FadeIn(eq1[6]), run_time=0.4)
        self.play(Indicate(v2l, color=GOLD, scale_factor=2.0), run_time=0.6)
        self.play(FadeIn(eq1[7]), run_time=0.4); self.wait(0.5)

        eq2 = MathTex(r"Q^\star(x_0,a_2)",r"=",r"0.8",r"+\,0.8",r"\!\cdot\!1.0",
                      r"+\,0.2",r"\!\cdot\!1.28",r"=1.856",
                      font_size=16, color=WHITE).next_to(eq1, DOWN, buff=0.15, aligned_edge=LEFT)
        self.play(FadeIn(eq2[0]),FadeIn(eq2[1]), run_time=0.3)
        self.play(Indicate(self.act_dots["x0"][1], color=GOLD, scale_factor=2.0), run_time=0.5)
        self.play(FadeIn(eq2[2]), run_time=0.3)
        self.play(Indicate(self.info_txts["x0"][1], color=GOLD, scale_factor=1.5), run_time=0.5)
        self.play(FadeIn(eq2[3]), run_time=0.3)
        self.play(Indicate(self.trans_arrows[0], color=SOFT_BLUE, scale_factor=1.3), run_time=0.5)
        self.play(FadeIn(eq2[4]), run_time=0.3)
        self.play(Indicate(v1l, color=GOLD, scale_factor=2.0), run_time=0.5)
        self.play(FadeIn(eq2[5]), run_time=0.3)
        self.play(Indicate(self.trans_arrows[1], color=PINK, scale_factor=1.3), run_time=0.5)
        self.play(FadeIn(eq2[6]), run_time=0.3)
        self.play(Indicate(v2l, color=GOLD, scale_factor=2.0), run_time=0.5)
        self.play(FadeIn(eq2[7]), run_time=0.3); self.wait(0.5)

        c6b = cap("Pick the larger Q.")
        self.play(FadeTransform(c6, c6b))
        win = SurroundingRectangle(eq2, color=TEAL, buff=0.04, stroke_width=2)
        self.play(Create(win)); self.wait(0.8)
        spv = MathTex(r"V^\star(x_0)=\max\{1.228,1.856\}=1.856\;\;(a_2)", font_size=16, color=GOLD)
        spv.next_to(eq2, DOWN, buff=0.15, aligned_edge=LEFT)
        self.play(Write(spv), run_time=0.8); self.wait(1)
        v0 = MathTex(r"V^\star\!=\!1.856", font_size=14, color=GOLD)
        v0.next_to(self.circles["x0"], UP, buff=0.08)
        self.play(FadeIn(v0), FadeOut(eq1),FadeOut(eq2),FadeOut(spv),FadeOut(win),FadeOut(hl))
        self.wait(0.5)

        # Final
        c7 = cap("The optimal value at x₀\nis 1.856, achieved by\nchoosing a₂ everywhere.")
        self.play(FadeTransform(c6b, c7))
        result = MathTex(r"V_0^\star(x_0)=1.856", font_size=30, color=GOLD).to_edge(UP, buff=0.4)
        rb = SurroundingRectangle(result, color=ACCENT, buff=0.12, stroke_width=3)
        an = MathTex(r"\pi^\star(\cdot)=a_2\;\;\forall\,x", font_size=24, color=ACCENT)
        an.next_to(rb, DOWN, buff=0.15)
        self.play(Write(result), Create(rb), run_time=1)
        self.play(FadeIn(an)); self.wait(3)

        # OUTRO
        all_s = Group(*self.mobjects)
        self.play(FadeOut(all_s), run_time=1.5)
        outro = Text("Backward induction gives\nthe optimal policy and\nvalue function.",
                      font_size=30, color=WHITE, line_spacing=1.2)
        self.play(FadeIn(outro, shift=UP*0.2)); self.wait(2)
        self.play(FadeOut(outro)); self.wait(0.5)
