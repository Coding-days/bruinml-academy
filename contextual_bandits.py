from manim import *
import numpy as np


class ContextualBanditsVideo(Scene):
    def construct(self):
        def cap(text):
            return Text(text, font_size=22, color=WHITE, line_spacing=0.8).to_edge(DOWN, buff=0.25)

        def swap(old, new_text):
            new = cap(new_text)
            if old is not None:
                self.play(FadeOut(old), FadeIn(new), run_time=0.5)
            else:
                self.play(FadeIn(new), run_time=0.5)
            return new

        def clear():
            self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.7)

        def slabel(text, color=GREY_B):
            return Text(text, font_size=18, color=color, slant=ITALIC)

        c = None

        # ═══════════════════════════════════════════════════════
        #  TITLE
        # ═══════════════════════════════════════════════════════
        title = Text("Contextual Bandits", font_size=48, color=BLUE)
        sub = Text("From Multi-Armed Bandits\nto Linear Models", font_size=26).next_to(title, DOWN, 0.5)
        self.play(Write(title), run_time=1.5)
        self.play(FadeIn(sub))
        self.wait(1.5)
        clear()

        # ═══════════════════════════════════════════════════════
        #  1  STANDARD MAB
        # ═══════════════════════════════════════════════════════
        c = swap(None, "Consider a standard\nmulti-armed bandit.")
        machine_colors = [RED, GREEN, YELLOW, TEAL]
        machines = VGroup()
        for i, col in enumerate(machine_colors):
            x = -3.5 + i * 2.3
            body = RoundedRectangle(width=1.2, height=1.6, corner_radius=0.12, color=col, fill_opacity=0.2, stroke_width=2.5).move_to(RIGHT * x + UP * 0.8)
            label = MathTex(f"a_{i+1}", font_size=26).move_to(body)
            mu = MathTex(r"\mu_{" + str(i+1) + r"}", font_size=20, color=col).next_to(body, DOWN, 0.15)
            machines.add(VGroup(body, label, mu))
        q_marks = VGroup(*[Text("?", font_size=30, color=GREY).move_to(m[0].get_center() + UP * 0.35) for m in machines])
        self.play(LaggedStart(*[FadeIn(m) for m in machines], lag_ratio=0.15))
        self.play(LaggedStart(*[FadeIn(q) for q in q_marks], lag_ratio=0.1))
        self.wait(1)

        c = swap(c, "Each arm has its own\nunknown mean reward.")
        brace = Brace(VGroup(*[m[2] for m in machines]), DOWN, buff=0.15, color=GREY)
        brace_label = Text("K separate unknowns", font_size=20, color=GREY).next_to(brace, DOWN, 0.1)
        self.play(Create(brace), Write(brace_label))
        self.wait(1)

        c = swap(c, "We estimated each μ_k\nwith the empirical mean.")
        emp_mean_eq = MathTex(r"\widehat{\mu}_k = \frac{1}{N_k}\sum_{i=1}^{N_k} r_i", font_size=32, color=GOLD).move_to(DOWN * 2)
        emp_label = slabel("(empirical mean of arm k's rewards)", GOLD).next_to(emp_mean_eq, DOWN, 0.2)
        self.play(Write(emp_mean_eq), FadeIn(emp_label))
        self.wait(2)
        clear()

        # ═══════════════════════════════════════════════════════
        #  2  ADD CONTEXT
        # ═══════════════════════════════════════════════════════
        c = swap(None, "Now suppose each arm\ncomes with a context.")
        learner = VGroup(
            RoundedRectangle(width=1.6, height=0.8, corner_radius=0.1, color=BLUE, fill_opacity=0.2),
            Text("Learner", font_size=18),
        ).arrange(ORIGIN).move_to(LEFT * 4.5 + UP * 0.5)
        arm_specs = [(UP * 1.5, RED, "a_1"), (ORIGIN, GREEN, "a_2"), (DOWN * 1.5, YELLOW, "a_3")]
        arms_g = VGroup(); ctx_bubbles = VGroup(); arrows_g = VGroup()
        for offset, col, a_lbl in arm_specs:
            pos = RIGHT * 0 + offset
            circ = Circle(radius=0.35, color=col, fill_opacity=0.2).move_to(pos)
            al = MathTex(a_lbl, font_size=24).move_to(pos)
            arr = Arrow(learner.get_right(), circ.get_left(), buff=0.1, color=GREY, stroke_width=2, max_tip_length_to_length_ratio=0.12)
            ctx_rect = RoundedRectangle(width=2.0, height=0.5, corner_radius=0.08, color=col, fill_opacity=0.1).next_to(circ, RIGHT, 0.3)
            ctx_lbl = MathTex(r"x_t(" + a_lbl + r") \in \mathbb{R}^d", font_size=20, color=col).move_to(ctx_rect)
            arms_g.add(VGroup(circ, al)); ctx_bubbles.add(VGroup(ctx_rect, ctx_lbl)); arrows_g.add(arr)
        self.play(FadeIn(learner))
        self.play(LaggedStart(*[FadeIn(a) for a in arms_g], lag_ratio=0.12), LaggedStart(*[GrowArrow(a) for a in arrows_g], lag_ratio=0.12))
        self.wait(0.5)
        c = swap(c, "The context is a\nfeature vector we observe.")
        for cb in ctx_bubbles:
            self.play(FadeIn(cb, shift=RIGHT * 0.3), run_time=0.4)
        obs_label = Text("observable!", font_size=22, color=GREEN).move_to(RIGHT * 3.5 + UP * 2.2)
        obs_arrow = Arrow(obs_label.get_bottom(), ctx_bubbles[0].get_right() + RIGHT * 0.1, color=GREEN, stroke_width=2, max_tip_length_to_length_ratio=0.12)
        self.play(Write(obs_label), GrowArrow(obs_arrow))
        self.wait(2)
        clear()

        # ═══════════════════════════════════════════════════════
        #  3  LINEAR REWARD + SHARED θ*
        # ═══════════════════════════════════════════════════════
        c = swap(None, "Reward is linear\nin the context vector.")
        eq_model = MathTex(r"\mathbb{E}[r_t(a) \mid x_t(a)]", r"=", r"\langle x_t(a),\;\theta^\star \rangle", font_size=32).move_to(UP * 2)
        self.play(Write(eq_model)); self.wait(1)
        noise_eq = MathTex(r"r_t = \langle x_t(a_t),\;\theta^\star \rangle + \eta_t", font_size=30).next_to(eq_model, DOWN, 0.6)
        c = swap(c, "We observe a noisy\nversion of this reward.")
        self.play(Write(noise_eq)); self.wait(1.5)
        c = swap(c, "The key difference:\nθ* is shared by all arms.")
        shared_box = VGroup(
            RoundedRectangle(width=4.5, height=1.0, corner_radius=0.12, color=GOLD, fill_opacity=0.15, stroke_width=2.5),
            MathTex(r"\text{One }\theta^\star \in \mathbb{R}^d\text{ for all arms}", font_size=26, color=GOLD),
        ).arrange(ORIGIN).move_to(DOWN * 0.6)
        self.play(FadeIn(shared_box, scale=1.05)); self.wait(1)
        c = swap(c, "Pulling one arm teaches\nus about every arm.")
        insight = Text("→ shared structure lets us\n   generalize across arms", font_size=22, color=TEAL).move_to(DOWN * 2)
        self.play(FadeIn(insight, shift=UP * 0.2))
        self.wait(2)
        clear()

        # ═══════════════════════════════════════════════════════
        #  4  BEST ARM CHANGES
        # ═══════════════════════════════════════════════════════
        c = swap(None, "But unlike standard bandits,\nthe best arm can change.")
        theta_disp = MathTex(r"\theta^\star = (1,\;-1)", font_size=32, color=GOLD).to_edge(UP, buff=0.6)
        self.play(Write(theta_disp))
        sep = DashedLine(UP * 2, DOWN * 2.2, color=GREY, stroke_width=1)
        lt = Text("Round 1", font_size=22, color=BLUE_C).move_to(LEFT * 3.2 + UP * 1.5)
        lc1 = MathTex(r"x(a_1)=(2,3)", font_size=25).move_to(LEFT * 3.2 + UP * 0.8)
        lc2 = MathTex(r"x(a_2)=(4,-1)", font_size=25).move_to(LEFT * 3.2 + UP * 0.2)
        lr1 = MathTex(r"\langle(2,3),(1,-1)\rangle=-1", font_size=22, color=RED).move_to(LEFT * 3.2 + DOWN * 0.5)
        lr2 = MathTex(r"\langle(4,-1),(1,-1)\rangle=5", font_size=22, color=GREEN).move_to(LEFT * 3.2 + DOWN * 1.1)
        lb = Text("Arm 2 wins", font_size=20, color=GREEN).move_to(LEFT * 3.2 + DOWN * 1.7)
        self.play(Write(lt)); self.play(Write(lc1), Write(lc2)); self.play(Write(lr1), Write(lr2)); self.play(FadeIn(lb)); self.wait(1)
        c = swap(c, "Swap the contexts\nand the winner flips.")
        self.play(Create(sep))
        rt = Text("Round 2", font_size=22, color=BLUE_C).move_to(RIGHT * 3.2 + UP * 1.5)
        rc1 = MathTex(r"x(a_1)=(4,-1)", font_size=25).move_to(RIGHT * 3.2 + UP * 0.8)
        rc2 = MathTex(r"x(a_2)=(2,3)", font_size=25).move_to(RIGHT * 3.2 + UP * 0.2)
        rr1 = MathTex(r"\langle(4,-1),(1,-1)\rangle=5", font_size=22, color=GREEN).move_to(RIGHT * 3.2 + DOWN * 0.5)
        rr2 = MathTex(r"\langle(2,3),(1,-1)\rangle=-1", font_size=22, color=RED).move_to(RIGHT * 3.2 + DOWN * 1.1)
        rb = Text("Arm 1 wins", font_size=20, color=GREEN).move_to(RIGHT * 3.2 + DOWN * 1.7)
        self.play(Write(rt)); self.play(Write(rc1), Write(rc2)); self.play(Write(rr1), Write(rr2)); self.play(FadeIn(rb))
        self.wait(2)
        clear()

        # ═══════════════════════════════════════════════════════
        #  5  TRANSITION → LEAST SQUARES
        # ═══════════════════════════════════════════════════════
        c = swap(None, "So the whole problem\nreduces to estimating θ*.")
        big_q = MathTex(r"\text{How do we estimate }\theta^\star\text{ from data?}", font_size=32, color=GOLD).move_to(UP * 1)
        self.play(Write(big_q)); self.wait(1.5)
        c = swap(c, "We have context vectors\nand noisy rewards.")
        data_eq = MathTex(r"\text{Data: }\;(x_1, r_1),\;(x_2, r_2),\;\dots,\;(x_t, r_t)", font_size=26).move_to(DOWN * 0)
        model_eq = MathTex(r"r_s \approx \langle x_s,\;\theta^\star\rangle", font_size=28).next_to(data_eq, DOWN, 0.5)
        self.play(Write(data_eq)); self.play(Write(model_eq)); self.wait(1)
        c = swap(c, "Answer: least squares.")
        answer = Text("→ Least Squares", font_size=34, color=BLUE).move_to(DOWN * 2)
        self.play(FadeIn(answer, scale=1.1))
        self.wait(2)
        clear()

        # ═══════════════════════════════════════════════════════
        #  6  LEAST SQUARES 1-D = EMPIRICAL MEAN
        # ═══════════════════════════════════════════════════════
        c = swap(None, "But least squares\nis not a new idea.")
        ls_title = Text("Least Squares", font_size=38, color=BLUE).to_edge(UP, buff=0.5)
        self.play(Write(ls_title)); self.wait(0.5)
        c = swap(c, "Remember the empirical\nmean from standard bandits?")
        recall_box = VGroup(
            RoundedRectangle(width=6, height=1.2, corner_radius=0.1, color=GOLD, fill_opacity=0.1, stroke_width=2),
            VGroup(Text("Standard MAB:", font_size=20, color=GOLD),
                   MathTex(r"\widehat{\mu}_k = \frac{1}{N_k}\sum_{i=1}^{N_k} r_i", font_size=28, color=GOLD)).arrange(RIGHT, buff=0.4),
        ).arrange(ORIGIN).move_to(UP * 1.2)
        self.play(FadeIn(recall_box)); self.wait(1.5)
        c = swap(c, "It turns out this IS\nleast squares in disguise.")
        obj = MathTex(r"\min_{x \in \mathbb{R}}\;\sum_{i=1}^n (x - r_i)^2", font_size=32).move_to(DOWN * 0.2)
        obj_label = slabel("(minimize squared error)", GREY_B).next_to(obj, RIGHT, 0.3)
        self.play(Write(obj), FadeIn(obj_label)); self.wait(1.5)
        self.play(FadeOut(recall_box), FadeOut(ls_title))
        self.play(obj.animate.move_to(UP * 2.5), obj_label.animate.move_to(UP * 2.5 + RIGHT * 3.8))

        c = swap(c, "Let's verify.\nDefine the objective.")
        f_def = MathTex(r"f(x) = \sum_{i=1}^n (x - r_i)^2", font_size=30).move_to(UP * 1.5)
        f_label = slabel("define objective", GREY_B).next_to(f_def, LEFT, 0.4)
        self.play(Write(f_def), FadeIn(f_label)); self.wait(1)

        c = swap(c, "Take the derivative\nand set it to zero.")
        deriv = MathTex(r"f'(x) = 2\!\left(nx - \sum_{i=1}^n r_i\right)", font_size=28).move_to(UP * 0.4)
        deriv_label = slabel("take derivative", GREY_B).next_to(deriv, LEFT, 0.4)
        self.play(Write(deriv), FadeIn(deriv_label)); self.wait(1)
        set_zero = MathTex(r"2\!\left(nx - \sum_{i=1}^n r_i\right) = 0", font_size=28).move_to(DOWN * 0.5)
        zero_label = slabel("set to zero", GREY_B).next_to(set_zero, LEFT, 0.4)
        self.play(Write(set_zero), FadeIn(zero_label)); self.wait(1)

        c = swap(c, "Solve for x.\nIt's the empirical mean!")
        sol = MathTex(r"x^\star = \frac{1}{n}\sum_{i=1}^n r_i", font_size=36, color=GOLD).move_to(DOWN * 1.6)
        sol_label = slabel("solve for x", GOLD).next_to(sol, LEFT, 0.4)
        self.play(Write(sol), FadeIn(sol_label)); self.wait(1)
        conn_box = SurroundingRectangle(sol, color=GOLD, buff=0.15, stroke_width=2.5)
        conn_text = Text("= same estimator as MAB!", font_size=22, color=GOLD).next_to(conn_box, RIGHT, 0.3)
        self.play(Create(conn_box), Write(conn_text)); self.wait(2)
        self.play(*[FadeOut(m) for m in [obj, obj_label, f_def, f_label, deriv, deriv_label, set_zero, zero_label, sol, sol_label, conn_box, conn_text]])

        c = swap(c, "Visually: the mean\nminimizes total squared error.")
        ax = NumberLine(x_range=[0, 10, 1], length=9, include_numbers=True, font_size=18).shift(UP * 0.5)
        pts = [2, 4, 5, 7, 8]; mean_v = sum(pts) / len(pts)
        dots = VGroup(*[Dot(ax.n2p(p), color=BLUE, radius=0.08) for p in pts])
        self.play(Create(ax))
        self.play(LaggedStart(*[FadeIn(d, scale=0.5) for d in dots], lag_ratio=0.12))
        mean_line = DashedLine(ax.n2p(mean_v) + UP * 0.7, ax.n2p(mean_v) + DOWN * 0.7, color=GOLD, stroke_width=3)
        mean_lbl = MathTex(r"\bar{r}=5.2", font_size=24, color=GOLD).next_to(mean_line, UP, 0.1)
        self.play(Create(mean_line), Write(mean_lbl))
        err_lines = VGroup(*[Line(ax.n2p(p) + UP * 0.12, ax.n2p(mean_v) + UP * 0.12, color=RED, stroke_width=2) for p in pts])
        self.play(LaggedStart(*[Create(e) for e in err_lines], lag_ratio=0.1))
        self.wait(2)
        clear()

        # ═══════════════════════════════════════════════════════
        #  7  VECTOR LEAST SQUARES
        # ═══════════════════════════════════════════════════════
        c = swap(None, "Now generalize:\nfit θ in R^d\ninstead of one number.")
        compare_title = Text("Scalar → Vector", font_size=30, color=BLUE).to_edge(UP, buff=0.5)
        self.play(Write(compare_title))
        scalar_eq = MathTex(r"\min_x \sum_i (x - r_i)^2", font_size=26).move_to(LEFT * 3 + UP * 1.2)
        scalar_box = SurroundingRectangle(scalar_eq, color=GREY, buff=0.12, stroke_width=1.5)
        scalar_lbl = Text("1-D  (standard MAB)", font_size=18, color=GREY).next_to(scalar_box, DOWN, 0.15)
        vec_eq = MathTex(r"\min_\theta \sum_i (r_i - \langle a_i, \theta\rangle)^2", font_size=26).move_to(RIGHT * 3 + UP * 1.2)
        vec_box = SurroundingRectangle(vec_eq, color=BLUE, buff=0.12, stroke_width=1.5)
        vec_lbl = Text("d-D  (contextual bandit)", font_size=18, color=BLUE).next_to(vec_box, DOWN, 0.15)
        big_arrow = MathTex(r"\Longrightarrow", font_size=36).move_to(UP * 1.2)
        self.play(Write(scalar_eq), Create(scalar_box), FadeIn(scalar_lbl))
        self.play(Write(big_arrow))
        self.play(Write(vec_eq), Create(vec_box), FadeIn(vec_lbl)); self.wait(2)

        c = swap(c, "Same idea, same steps,\njust in higher dimensions.")
        self.play(FadeOut(compare_title), FadeOut(scalar_eq), FadeOut(scalar_box), FadeOut(scalar_lbl), FadeOut(big_arrow), FadeOut(vec_box), FadeOut(vec_lbl),
                  vec_eq.animate.move_to(UP * 2.5).set_color(WHITE))

        s1_label = slabel("take gradient", GREY_B)
        grad_eq = MathTex(r"\sum_{i=1}^n \bigl(r_i - a_i^\top\theta\bigr)\,a_i = 0", font_size=28).move_to(UP * 1.3)
        s1_label.next_to(grad_eq, LEFT, 0.3)
        c = swap(c, "Take the gradient\nand set it to zero.")
        self.play(Write(grad_eq), FadeIn(s1_label)); self.wait(1)

        s2_label = slabel("outer-product identity", TEAL)
        identity = MathTex(r"(a_i^\top \theta)\,a_i = (a_i a_i^\top)\,\theta", font_size=26, color=TEAL).move_to(UP * 0.3)
        s2_label.next_to(identity, LEFT, 0.3)
        c = swap(c, "Use the outer-product\nidentity to rewrite.")
        self.play(Write(identity), FadeIn(s2_label)); self.wait(1)

        s3_label = slabel("rearrange", GREY_B)
        normal = MathTex(r"\left(\sum_{i=1}^n a_i a_i^\top\right)\theta = \sum_{i=1}^n a_i\, r_i", font_size=26).move_to(DOWN * 0.7)
        s3_label.next_to(normal, LEFT, 0.3)
        c = swap(c, "Collect terms into\nthe normal equation.")
        self.play(Write(normal), FadeIn(s3_label)); self.wait(1.5)
        self.play(FadeOut(vec_eq), FadeOut(grad_eq), FadeOut(s1_label), FadeOut(identity), FadeOut(s2_label), FadeOut(normal), FadeOut(s3_label))

        c = swap(c, "Define V and b\nfor compact notation.")
        s4_label = slabel("define V and b", GREY_B)
        vb = VGroup(MathTex(r"V = \sum_{i=1}^n a_i a_i^\top", font_size=28), MathTex(r"b = \sum_{i=1}^n a_i\, r_i", font_size=28)).arrange(RIGHT, buff=1.2).move_to(UP * 1.5)
        s4_label.next_to(vb, LEFT, 0.3)
        self.play(Write(vb), FadeIn(s4_label)); self.wait(0.8)
        s5_label = slabel("normal equation", GOLD)
        compact_eq = MathTex(r"V\theta = b", font_size=40, color=GOLD).move_to(UP * 0.2)
        s5_label.next_to(compact_eq, LEFT, 0.5)
        self.play(Write(compact_eq), FadeIn(s5_label)); self.wait(0.8)

        c = swap(c, "If V is invertible,\nwe get our estimate.")
        s6_label = slabel("solve", GOLD)
        sol_vec = MathTex(r"\widehat{\theta} = V^{-1}b", font_size=42, color=GOLD).move_to(DOWN * 1)
        s6_label.next_to(sol_vec, LEFT, 0.5)
        self.play(Write(sol_vec), FadeIn(s6_label)); self.wait(2)
        clear()

        # ═══════════════════════════════════════════════════════
        #  8  V_t IN BANDITS + REGULARIZATION
        # ═══════════════════════════════════════════════════════
        c = swap(None, "In the bandit setting,\nwe update V each round.")
        vt = MathTex(r"V_t = \lambda I + \sum_{s=1}^t A_s A_s^\top", font_size=34, color=BLUE).move_to(UP * 2.2)
        self.play(Write(vt)); self.wait(0.8)
        theta_hat = MathTex(r"\widehat{\theta}_t = V_t^{-1} \sum_{s=1}^t A_s X_s", font_size=30).next_to(vt, DOWN, 0.5)
        c = swap(c, "This gives us the\nleast-squares estimate of θ*.")
        self.play(Write(theta_hat)); self.wait(1.5)

        # ── REGULARIZATION ASIDE ──
        c = swap(c, "Why the λI term?\nThis is regularization.")
        reg_title = Text("Regularization", font_size=26, color=TEAL).move_to(UP * 0.2)
        self.play(Write(reg_title)); self.wait(0.8)

        c = swap(c, "It solves a modified\nobjective that penalizes\nlarge θ.")
        reg_obj = MathTex(
            r"\min_\theta\;\underbrace{\sum_{s=1}^t \bigl(r_s - \langle x_s,\theta\rangle\bigr)^2}_{\text{data fit}}",
            r"+\;\underbrace{\lambda \|\theta\|^2}_{\text{prefer small }\theta}",
            font_size=24,
        ).move_to(DOWN * 0.8)
        self.play(Write(reg_obj)); self.wait(2)

        c = swap(c, "Why is this valid?\nIf θ* is optimal,\nso is cθ* for c > 0.")
        scale_eq = MathTex(
            r"\arg\max_a \langle x(a),\,\theta^\star\rangle",
            r"=",
            r"\arg\max_a \langle x(a),\,c\,\theta^\star\rangle",
            font_size=26,
        ).move_to(DOWN * 2)
        scale_label = slabel("scaling doesn't change the best arm", TEAL).next_to(scale_eq, DOWN, 0.2)
        self.play(Write(scale_eq), FadeIn(scale_label)); self.wait(2)

        c = swap(c, "So we lose nothing by\npreferring smaller θ.\nIt also ensures V_t\nis invertible.")
        self.wait(2)
        clear()

        # ═══════════════════════════════════════════════════════
        #  9  POSITIVE DEFINITENESS
        # ═══════════════════════════════════════════════════════
        c = swap(None, "But does V_t^{-1}\nalways exist?")
        q_inv = MathTex(r"V_t^{-1}\;\text{exists}\;?", font_size=34, color=YELLOW).move_to(UP * 1)
        self.play(Write(q_inv)); self.wait(1)
        self.play(FadeOut(q_inv))

        c = swap(c, "Yes. Each outer product\nis positive semidefinite.")
        s_psd = slabel("outer product is PSD", GREY_B)
        psd_eq = MathTex(r"x^\top\!(A_s A_s^\top)\,x = (A_s^\top x)^2 \ge 0", font_size=28).move_to(UP * 2)
        s_psd.next_to(psd_eq, LEFT, 0.3)
        self.play(Write(psd_eq), FadeIn(s_psd)); self.wait(1)

        c = swap(c, "Sums of PSD matrices\nare still PSD.")
        s_sum = slabel("sum preserves PSD", GREY_B)
        sum_psd = MathTex(r"\sum_{s=1}^t A_s A_s^\top \succeq 0", font_size=28).move_to(UP * 0.8)
        s_sum.next_to(sum_psd, LEFT, 0.3)
        self.play(Write(sum_psd), FadeIn(s_sum)); self.wait(1)

        c = swap(c, "Adding λI makes it\nstrictly positive definite.")
        s_pd = slabel("regularization", GREEN)
        pd_line = MathTex(r"\lambda > 0 \;\Longrightarrow\; V_t = \lambda I + \sum A_s A_s^\top \succ 0", font_size=24, color=GREEN).move_to(DOWN * 0.2)
        s_pd.next_to(pd_line, LEFT, 0.3)
        self.play(Write(pd_line), FadeIn(s_pd)); self.wait(0.8)
        s_inv = slabel("invertible", GREEN)
        inv_line = MathTex(r"\Longrightarrow\; V_t^{-1}\text{ exists } \checkmark", font_size=28, color=GREEN).move_to(DOWN * 1.1)
        s_inv.next_to(inv_line, LEFT, 0.3)
        self.play(Write(inv_line), FadeIn(s_inv)); self.wait(1)

        c = swap(c, "And V_t only grows:\nmore data, more information.")
        s_mono = slabel("monotonicity", YELLOW)
        mono = MathTex(r"V_t - V_{t-1} = A_t A_t^\top \succeq 0", font_size=28, color=YELLOW).move_to(DOWN * 2.1)
        s_mono.next_to(mono, LEFT, 0.3)
        self.play(Write(mono), FadeIn(s_mono)); self.wait(2)
        clear()

        # ═══════════════════════════════════════════════════════
        # 10  CONFIDENCE ELLIPSOID
        # ═══════════════════════════════════════════════════════
        c = swap(None, "We have an estimate.\nBut how confident are we?")
        hat_theta = MathTex(r"\widehat{\theta}_t \approx \theta^\star \;\;?", font_size=36, color=GOLD).move_to(UP * 1)
        self.play(Write(hat_theta)); self.wait(1.5)
        c = swap(c, "V_t also defines a\nconfidence region around θ*.")
        conf = MathTex(r"\mathcal{E}_t = \bigl\{\theta : \|\theta - \widehat{\theta}_t\|_{V_t}^2 \le \beta_t \bigr\}", font_size=28).move_to(DOWN * 0.2)
        self.play(Write(conf)); self.wait(1)
        c = swap(c, "What shape does\nthis region have?")
        shape_q = MathTex(r"\|\cdot\|_{V_t}\;\text{is the elliptical norm}", font_size=26, color=TEAL).next_to(conf, DOWN, 0.6)
        self.play(Write(shape_q)); self.wait(2)
        clear()

        # ═══════════════════════════════════════════════════════
        # 11  CIRCLE EXAMPLE — SLOW, STEP BY STEP
        # ═══════════════════════════════════════════════════════
        c = swap(None, "Let's compute an example\nstep by step.")

        circ_title = Text("Example: circular confidence set", font_size=26, color=BLUE).to_edge(UP, buff=0.5)
        self.play(Write(circ_title))

        # Step 1: state V
        c = swap(c, "Suppose V is diagonal\nwith equal entries.")
        s_v = slabel("given V", GREY_B)
        v_eq = MathTex(r"V = \begin{bmatrix} 4 & 0 \\ 0 & 4 \end{bmatrix}", font_size=30).move_to(UP * 1.5)
        s_v.next_to(v_eq, LEFT, 0.4)
        self.play(Write(v_eq), FadeIn(s_v)); self.wait(1.5)

        # Step 2: invert
        c = swap(c, "Diagonal matrices are\neasy to invert:\njust invert each entry.")
        s_inv2 = slabel("invert V", GREY_B)
        vinv_eq = MathTex(r"V^{-1} = \begin{bmatrix} 1/4 & 0 \\ 0 & 1/4 \end{bmatrix}", font_size=30).move_to(UP * 0.3)
        s_inv2.next_to(vinv_eq, LEFT, 0.4)
        self.play(Write(vinv_eq), FadeIn(s_inv2)); self.wait(1.5)

        # Step 3: compute x^T V^{-1} x
        c = swap(c, "Now compute the\nquadratic form x⊤V⁻¹x.")
        s_quad = slabel("quadratic form", GREY_B)
        quad_eq = MathTex(
            r"x^\top V^{-1} x",
            r"= (x_1,\,x_2)",
            r"\begin{bmatrix} 1/4 & 0 \\ 0 & 1/4 \end{bmatrix}",
            r"\begin{pmatrix} x_1 \\ x_2 \end{pmatrix}",
            font_size=24,
        ).move_to(DOWN * 0.7)
        s_quad.next_to(quad_eq, LEFT, 0.2)
        self.play(Write(quad_eq), FadeIn(s_quad)); self.wait(1.5)

        c = swap(c, "Multiply it out.")
        s_expand = slabel("expand", GREY_B)
        expand_eq = MathTex(
            r"= \frac{x_1^2}{4} + \frac{x_2^2}{4}",
            r"= \frac{x_1^2 + x_2^2}{4}",
            font_size=28,
        ).move_to(DOWN * 1.7)
        s_expand.next_to(expand_eq, LEFT, 0.3)
        self.play(Write(expand_eq), FadeIn(s_expand)); self.wait(1.5)
        clear()

        # Step 4: the set
        c = swap(c, "Setting this ≤ 1\ngives us the confidence set.")

        set_eq1 = MathTex(r"\{x : x^\top V^{-1} x \le 1\}", font_size=28).move_to(UP * 2)
        self.play(Write(set_eq1)); self.wait(1)

        s_sub = slabel("substitute", GREY_B)
        set_eq2 = MathTex(r"\frac{x_1^2 + x_2^2}{4} \le 1", font_size=30).move_to(UP * 1)
        s_sub.next_to(set_eq2, LEFT, 0.4)
        self.play(Write(set_eq2), FadeIn(s_sub)); self.wait(1)

        c = swap(c, "Multiply both sides by 4.")
        s_simp = slabel("simplify", GREY_B)
        set_eq3 = MathTex(r"x_1^2 + x_2^2 \le 4", font_size=32, color=BLUE).move_to(UP * 0)
        s_simp.next_to(set_eq3, LEFT, 0.4)
        self.play(Write(set_eq3), FadeIn(s_simp)); self.wait(1)

        c = swap(c, "This is a circle\nof radius 2.")
        radius_note = MathTex(r"\text{radius} = \sqrt{4} = 2", font_size=26, color=BLUE).next_to(set_eq3, DOWN, 0.5)
        self.play(Write(radius_note)); self.wait(1)

        # draw circle
        axes_c = Axes(x_range=[-3, 3, 1], y_range=[-3, 3, 1], x_length=3.5, y_length=3.5,
                      axis_config={"include_tip": True, "tip_length": 0.1, "include_numbers": False}).move_to(DOWN * 1.5 + RIGHT * 3)
        uc = 3.5 / 6
        circ_shape = Circle(radius=2 * uc, color=BLUE, stroke_width=3, fill_opacity=0.1, fill_color=BLUE).move_to(axes_c.c2p(0, 0))
        self.play(Create(axes_c), Create(circ_shape)); self.wait(2)
        clear()

        # ═══════════════════════════════════════════════════════
        # 12  ELLIPSE EXAMPLE — SLOW, STEP BY STEP
        # ═══════════════════════════════════════════════════════
        c = swap(None, "Now try unequal\ndiagonal entries.")

        ell_title = Text("Example: elliptical confidence set", font_size=26, color=GOLD).to_edge(UP, buff=0.5)
        self.play(Write(ell_title))

        # Step 1: state V
        c = swap(c, "This time the diagonal\nentries differ.")
        s_v2 = slabel("given V", GREY_B)
        v2_eq = MathTex(r"V = \begin{bmatrix} 9 & 0 \\ 0 & 4 \end{bmatrix}", font_size=30).move_to(UP * 1.5)
        s_v2.next_to(v2_eq, LEFT, 0.4)
        self.play(Write(v2_eq), FadeIn(s_v2)); self.wait(1.5)

        # Step 2: invert
        c = swap(c, "Invert each diagonal entry.")
        s_inv3 = slabel("invert V", GREY_B)
        vinv2_eq = MathTex(r"V^{-1} = \begin{bmatrix} 1/9 & 0 \\ 0 & 1/4 \end{bmatrix}", font_size=30).move_to(UP * 0.3)
        s_inv3.next_to(vinv2_eq, LEFT, 0.4)
        self.play(Write(vinv2_eq), FadeIn(s_inv3)); self.wait(1.5)

        # Step 3: compute quadratic form
        c = swap(c, "Compute x⊤V⁻¹x\nby multiplying out.")
        s_quad2 = slabel("quadratic form", GREY_B)
        quad2_eq = MathTex(
            r"x^\top V^{-1} x",
            r"= \frac{x_1^2}{9} + \frac{x_2^2}{4}",
            font_size=28,
        ).move_to(DOWN * 0.7)
        s_quad2.next_to(quad2_eq, LEFT, 0.3)
        self.play(Write(quad2_eq), FadeIn(s_quad2)); self.wait(1.5)

        # Step 4: the set
        c = swap(c, "Setting this ≤ 1\ngives an ellipse.")
        s_set2 = slabel("confidence set", GOLD)
        set2_eq = MathTex(r"\frac{x_1^2}{9} + \frac{x_2^2}{4} \le 1", font_size=32, color=GOLD).move_to(DOWN * 1.7)
        s_set2.next_to(set2_eq, LEFT, 0.4)
        self.play(Write(set2_eq), FadeIn(s_set2)); self.wait(1.5)
        clear()

        # draw with annotations
        c = swap(c, "The semi-axes come from\nthe diagonal entries of V.")

        axes_e = Axes(x_range=[-4, 4, 1], y_range=[-3, 3, 1], x_length=5.5, y_length=4.5,
                      axis_config={"include_tip": True, "tip_length": 0.12, "include_numbers": False}).shift(LEFT * 1.5)
        xe_lab = MathTex("x_1", font_size=22).next_to(axes_e.x_axis, RIGHT, 0.1)
        ye_lab = MathTex("x_2", font_size=22).next_to(axes_e.y_axis, UP, 0.1)
        self.play(Create(axes_e), Write(xe_lab), Write(ye_lab))

        ue = 5.5 / 8
        uey = 4.5 / 6
        ell_shape = Ellipse(width=2 * 3 * ue, height=2 * 2 * uey, color=GOLD, stroke_width=3, fill_opacity=0.1, fill_color=GOLD).move_to(axes_e.c2p(0, 0))
        self.play(Create(ell_shape)); self.wait(1)

        # annotate semi-axes
        c = swap(c, "Semi-axis in x₁ direction:\n√9 = 3.")
        sa_h = DoubleArrow(axes_e.c2p(0, 0), axes_e.c2p(3, 0), buff=0, color=GOLD, stroke_width=2, max_tip_length_to_length_ratio=0.06)
        sa_h_lbl = MathTex(r"\sqrt{9}=3", font_size=22, color=GOLD).next_to(sa_h, DOWN, 0.1)
        self.play(Create(sa_h), Write(sa_h_lbl)); self.wait(1.5)

        c = swap(c, "Semi-axis in x₂ direction:\n√4 = 2.")
        sa_v = DoubleArrow(axes_e.c2p(0, 0), axes_e.c2p(0, 2), buff=0, color=GOLD, stroke_width=2, max_tip_length_to_length_ratio=0.08)
        sa_v_lbl = MathTex(r"\sqrt{4}=2", font_size=22, color=GOLD).next_to(sa_v, RIGHT, 0.1)
        self.play(Create(sa_v), Write(sa_v_lbl)); self.wait(1)

        # general rule
        rule_text = VGroup(
            MathTex(r"\text{Semi-axis length}", font_size=22),
            MathTex(r"= \sqrt{\text{diagonal entry of }V}", font_size=22, color=TEAL),
        ).arrange(DOWN, buff=0.15).move_to(RIGHT * 4 + UP * 1)
        self.play(FadeIn(rule_text)); self.wait(2)
        clear()

        # ═══════════════════════════════════════════════════════
        # 13  SHRINKING ELLIPSOID
        # ═══════════════════════════════════════════════════════
        c = swap(None, "As we collect data,\nthe ellipsoid shrinks.")
        axes4 = Axes(x_range=[-4, 4, 1], y_range=[-4, 4, 1], x_length=6, y_length=6,
                     axis_config={"include_tip": True, "tip_length": 0.12, "include_numbers": False})
        th1 = MathTex(r"\theta_1", font_size=22).next_to(axes4.x_axis, RIGHT, 0.1)
        th2 = MathTex(r"\theta_2", font_size=22).next_to(axes4.y_axis, UP, 0.1)
        self.play(Create(axes4), Write(th1), Write(th2))
        th_dot = Dot(axes4.c2p(0.5, -0.3), color=GOLD, radius=0.09)
        th_lbl = MathTex(r"\theta^\star", font_size=24, color=GOLD).next_to(th_dot, UR, 0.08)
        self.play(FadeIn(th_dot), Write(th_lbl))
        u4 = 6 / 8
        ell_specs = [(2.8, 2.2, BLUE_A, "t=1"), (2.0, 1.5, BLUE_B, "t=5"), (1.2, 0.9, BLUE_C, "t=20"), (0.5, 0.4, BLUE_D, "t=100")]
        drawn = []
        for w, h, col, lbl_text in ell_specs:
            e = Ellipse(width=2*w*u4, height=2*h*u4, color=col, stroke_width=2.5, fill_opacity=0.08, fill_color=col).move_to(axes4.c2p(0.5, -0.3))
            tlbl = MathTex(lbl_text, font_size=20, color=col).next_to(e, UR, 0.05)
            self.play(Create(e), Write(tlbl), run_time=0.8)
            for prev in drawn:
                prev.set_stroke(opacity=0.25); prev.set_fill(opacity=0.02)
            drawn.append(e)
            self.wait(0.4)
        c = swap(c, "More observations,\nless uncertainty about θ*.")
        self.wait(2)
        clear()

        # ═══════════════════════════════════════════════════════
        # 14  LinUCB ALGORITHM
        # ═══════════════════════════════════════════════════════
        c = swap(None, "Now: how do we\nuse this to choose arms?")
        linucb_title = Text("LinUCB", font_size=42, color=BLUE).to_edge(UP, buff=0.5)
        self.play(Write(linucb_title)); self.wait(0.5)

        c = swap(c, "Be optimistic: pick the θ\ninside the confidence set\nthat gives highest reward.")
        opt_eq = MathTex(r"a_t = \arg\max_{a \in \mathcal{A}_t}", r"\max_{\theta \in \mathcal{E}_t}", r"\langle x_t(a),\;\theta \rangle", font_size=28).move_to(UP * 1)
        opt_label_exploit = slabel("which arm?").next_to(opt_eq[0], DOWN, 0.25)
        opt_label_explore = slabel("optimistic θ", TEAL).next_to(opt_eq[1], DOWN, 0.25)
        self.play(Write(opt_eq))
        self.play(FadeIn(opt_label_exploit), FadeIn(opt_label_explore)); self.wait(2)

        c = swap(c, "The inner max has\na closed-form solution.")
        self.play(FadeOut(opt_label_exploit), FadeOut(opt_label_explore))
        closed_eq = MathTex(r"\max_{\theta \in \mathcal{E}_t}", r"\langle x,\;\theta \rangle", r"=",
                            r"\langle x,\;\widehat{\theta}_{t-1} \rangle", r"+", r"\sqrt{\beta_t}", r"\cdot", r"\|x\|_{V_{t-1}^{-1}}", font_size=26).move_to(DOWN * 0.3)
        self.play(Write(closed_eq)); self.wait(1)

        exploit_brace = Brace(closed_eq[3], DOWN, buff=0.1, color=GREEN)
        exploit_lbl = Text("exploit", font_size=18, color=GREEN).next_to(exploit_brace, DOWN, 0.05)
        explore_brace = Brace(VGroup(closed_eq[5], closed_eq[6], closed_eq[7]), DOWN, buff=0.1, color=RED)
        explore_lbl = Text("explore", font_size=18, color=RED).next_to(explore_brace, DOWN, 0.05)
        c = swap(c, "Exploit the current estimate,\nexplore uncertain directions.")
        self.play(Create(exploit_brace), FadeIn(exploit_lbl))
        self.play(Create(explore_brace), FadeIn(explore_lbl)); self.wait(2)
        clear()

        # ═══════════════════════════════════════════════════════
        # 15  LinUCB INDEX + UPDATES
        # ═══════════════════════════════════════════════════════
        c = swap(None, "So the LinUCB index\nfor each arm is:")
        ucb_formula = MathTex(r"\text{UCB}_t(a)", r"=", r"\langle x_t(a),\;\widehat{\theta}_{t-1} \rangle", r"+",
                              r"\sqrt{\beta_t}", r"\cdot \|x_t(a)\|_{V_{t-1}^{-1}}", font_size=28).move_to(UP * 1.5)
        ucb_box = SurroundingRectangle(ucb_formula, color=BLUE, buff=0.15, stroke_width=2.5)
        self.play(Write(ucb_formula), Create(ucb_box)); self.wait(1.5)

        c = swap(c, "Pull the arm with\nthe highest index.")
        rule = MathTex(r"a_t = \arg\max_{a \in \mathcal{A}_t}\;\text{UCB}_t(a)", font_size=30, color=GOLD).move_to(DOWN * 0)
        self.play(Write(rule)); self.wait(1)

        c = swap(c, "Then observe reward,\nupdate V_t and θ̂_t.")
        update_eqs = VGroup(
            MathTex(r"V_t \leftarrow V_{t-1} + x_t x_t^\top", font_size=26),
            MathTex(r"b_t \leftarrow b_{t-1} + x_t\, r_t", font_size=26),
            MathTex(r"\widehat{\theta}_t \leftarrow V_t^{-1}\, b_t", font_size=26),
        ).arrange(DOWN, buff=0.25, aligned_edge=LEFT).move_to(DOWN * 1.6)
        u_label = slabel("update step", GREY_B).next_to(update_eqs, LEFT, 0.3)
        self.play(Write(update_eqs), FadeIn(u_label)); self.wait(2)
        clear()

        # ═══════════════════════════════════════════════════════
        # 16  WORKED EXAMPLE
        # ═══════════════════════════════════════════════════════
        c = swap(None, "Let's walk through\na concrete example.")
        setup_title = Text("LinUCB Worked Example", font_size=32, color=BLUE).to_edge(UP, buff=0.5)
        self.play(Write(setup_title))
        setup_params = VGroup(
            MathTex(r"\theta^\star = (1,\;-1)", font_size=28, color=GOLD),
            MathTex(r"d = 2,\quad \lambda = 1,\quad \beta_t = 1", font_size=26),
            MathTex(r"\text{Two arms per round, noiseless rewards}", font_size=24, color=GREY_B),
        ).arrange(DOWN, buff=0.3).move_to(UP * 0.8)
        init = MathTex(r"V_0 = I,\quad b_0 = (0,0),\quad \widehat{\theta}_0 = (0,0)", font_size=26).move_to(DOWN * 0.5)
        self.play(Write(setup_params)); self.wait(1)
        c = swap(c, "Start with V_0 = I\nand θ̂_0 = (0,0).")
        self.play(Write(init)); self.wait(2)
        self.play(FadeOut(setup_title), FadeOut(setup_params), FadeOut(init))

        # TABLE HEADER
        col_x = [-5.2, -3.2, -1.2, 0.8, 2.3, 3.8, 5.3]
        header_texts = ["t", "UCB(a₁)", "UCB(a₂)", "Pull", "rₜ", "θ̂ₜ", "Vₜ diag"]
        headers = VGroup(*[Text(txt, font_size=16, color=BLUE_C).move_to(RIGHT * x_pos + UP * 2.5) for x_pos, txt in zip(col_x, header_texts)])
        header_line = Line(LEFT * 6.2 + UP * 2.25, RIGHT * 6.2 + UP * 2.25, color=GREY, stroke_width=1)
        self.play(FadeIn(headers), Create(header_line))

        # ──── ROUND 1 ────
        c = swap(c, "Round 1: x(a₁)=(1,0),\nx(a₂)=(0,1).")
        ctx_r1 = VGroup(MathTex(r"x(a_1)=(1,0)", font_size=22, color=RED), MathTex(r"x(a_2)=(0,1)", font_size=22, color=GREEN)).arrange(RIGHT, buff=0.8).move_to(UP * 1.7)
        self.play(FadeIn(ctx_r1)); self.wait(0.8)

        c = swap(c, "Both UCBs equal 1.\nTie-break: pull arm 1.")
        ucb1_calc = MathTex(r"0 + 1 \cdot 1 = 1.0", font_size=20, color=RED).move_to(LEFT * 2 + UP * 0.9)
        ucb2_calc = MathTex(r"0 + 1 \cdot 1 = 1.0", font_size=20, color=GREEN).move_to(RIGHT * 2 + UP * 0.9)
        self.play(Write(ucb1_calc), Write(ucb2_calc)); self.wait(1)

        r1_data = ["1", "1.00", "1.00", "a₁", "1", "(0.5, 0)", "(2, 1)"]
        row1 = VGroup(*[Text(val, font_size=15, color=(GREEN if val == "a₁" else WHITE)).move_to(RIGHT * x_pos + UP * 1.8) for x_pos, val in zip(col_x, r1_data)])
        self.play(FadeOut(ctx_r1), FadeOut(ucb1_calc), FadeOut(ucb2_calc), FadeIn(row1)); self.wait(1)

        # ──── ROUND 2 ────
        c = swap(c, "Round 2: x(a₁)=(0,1),\nx(a₂)=(1,0).")
        ctx_r2 = VGroup(MathTex(r"x(a_1)=(0,1)", font_size=22, color=RED), MathTex(r"x(a_2)=(1,0)", font_size=22, color=GREEN)).arrange(RIGHT, buff=0.8).move_to(UP * 0.9)
        self.play(FadeIn(ctx_r2)); self.wait(0.5)

        c = swap(c, "Arm 2 has higher UCB\nthanks to the exploit term.")
        ucb1_r2 = MathTex(r"0 + \sqrt{1} = 1.0", font_size=20, color=RED).move_to(LEFT * 2 + UP * 0.1)
        ucb2_r2 = MathTex(r"0.5 + \sqrt{0.5} \approx 1.21", font_size=20, color=GREEN).move_to(RIGHT * 2 + UP * 0.1)
        self.play(Write(ucb1_r2), Write(ucb2_r2)); self.wait(1)

        r2_data = ["2", "1.00", "1.21", "a₂", "1", "(0.67, 0)", "(3, 1)"]
        row2 = VGroup(*[Text(val, font_size=15, color=(GREEN if val == "a₂" else WHITE)).move_to(RIGHT * x_pos + UP * 1.3) for x_pos, val in zip(col_x, r2_data)])
        self.play(FadeOut(ctx_r2), FadeOut(ucb1_r2), FadeOut(ucb2_r2), FadeIn(row2)); self.wait(1)

        # ──── ROUND 3 ────
        c = swap(c, "Round 3: x(a₁)=(1,0),\nx(a₂)=(0,2).")
        ctx_r3 = VGroup(MathTex(r"x(a_1)=(1,0)", font_size=22, color=RED), MathTex(r"x(a_2)=(0,2)", font_size=22, color=GREEN)).arrange(RIGHT, buff=0.8).move_to(UP * 0.5)
        self.play(FadeIn(ctx_r3)); self.wait(0.5)

        c = swap(c, "Arm 2 has huge\nuncertainty in direction 2.\nHigh exploration bonus!")
        ucb1_r3 = MathTex(r"0.67 + \sqrt{1/3} \approx 1.24", font_size=20, color=RED).move_to(LEFT * 2 + DOWN * 0.3)
        ucb2_r3 = MathTex(r"0 + \sqrt{4} = 2.0", font_size=20, color=GREEN).move_to(RIGHT * 2 + DOWN * 0.3)
        self.play(Write(ucb1_r3), Write(ucb2_r3)); self.wait(1.5)

        r3_data = ["3", "1.24", "2.00", "a₂", "-2", "(0.67, -0.8)", "(3, 5)"]
        row3 = VGroup(*[Text(val, font_size=15, color=(GREEN if val == "a₂" else (RED if val == "-2" else WHITE))).move_to(RIGHT * x_pos + UP * 0.8) for x_pos, val in zip(col_x, r3_data)])
        self.play(FadeOut(ctx_r3), FadeOut(ucb1_r3), FadeOut(ucb2_r3), FadeIn(row3)); self.wait(1)

        c = swap(c, "Reward = -2!\nBut now we learned\nthat θ*₂ is negative.")
        conv_box = SurroundingRectangle(row3[5], color=GOLD, buff=0.08, stroke_width=2)
        conv_note = MathTex(r"\widehat{\theta}_3 = (0.67,\;-0.8) \;\approx\; \theta^\star = (1,\;-1)", font_size=22, color=GOLD).move_to(DOWN * 0.1)
        self.play(Create(conv_box), Write(conv_note)); self.wait(2)
        clear()

        # ═══════════════════════════════════════════════════════
        # 17  WHAT THE EXAMPLE SHOWS
        # ═══════════════════════════════════════════════════════
        c = swap(None, "Notice the pattern:")
        takeaway = VGroup(
            VGroup(Text("1.", font_size=24, color=BLUE), Text("Round 1-2: explore both", font_size=22), Text("coordinate directions", font_size=22)).arrange(RIGHT, buff=0.15),
            VGroup(Text("2.", font_size=24, color=BLUE), Text("Round 3: high uncertainty", font_size=22), Text("in direction 2 → explore it", font_size=22)).arrange(RIGHT, buff=0.15),
            VGroup(Text("3.", font_size=24, color=BLUE), Text("Negative reward teaches us", font_size=22), Text("θ*₂ < 0 — information gain!", font_size=22)).arrange(RIGHT, buff=0.15),
            VGroup(Text("4.", font_size=24, color=BLUE), Text("θ̂ converges:", font_size=22),
                   MathTex(r"(0,0) \to (0.5,0) \to (0.67,0) \to (0.67,-0.8)", font_size=20)).arrange(RIGHT, buff=0.15),
        ).arrange(DOWN, buff=0.4, aligned_edge=LEFT).move_to(UP * 0.5)
        for b in takeaway:
            self.play(FadeIn(b), run_time=0.7); self.wait(0.6)
        c = swap(c, "Exploration is targeted:\nwe explore where\nuncertainty is largest.")
        self.wait(2)
        clear()

        # ═══════════════════════════════════════════════════════
        # 18  RECAP
        # ═══════════════════════════════════════════════════════
        c = swap(None, "Putting it all together:")
        bullets = VGroup(
            VGroup(Text("1.", font_size=24, color=BLUE), Text("Context vectors let the best", font_size=22), Text("arm change each round", font_size=22)).arrange(RIGHT, buff=0.15),
            VGroup(Text("2.", font_size=24, color=BLUE), Text("Shared θ* → one", font_size=22), Text("estimation problem", font_size=22)).arrange(RIGHT, buff=0.15),
            VGroup(Text("3.", font_size=24, color=BLUE), Text("Regularized least squares =", font_size=22), Text("generalized empirical mean", font_size=22)).arrange(RIGHT, buff=0.15),
            VGroup(Text("4.", font_size=24, color=BLUE), Text("V_t shapes an ellipsoidal", font_size=22), Text("confidence set", font_size=22)).arrange(RIGHT, buff=0.15),
            VGroup(Text("5.", font_size=24, color=BLUE), Text("LinUCB = optimism over", font_size=22), Text("that ellipsoid", font_size=22)).arrange(RIGHT, buff=0.15),
        ).arrange(DOWN, buff=0.35, aligned_edge=LEFT).move_to(UP * 0.3)
        for b in bullets:
            self.play(FadeIn(b), run_time=0.7); self.wait(0.5)
        self.wait(2)
        clear()

        # END
        end1 = Text("Contextual Bandits", font_size=42, color=BLUE)
        end2 = Text("From Bandits to LinUCB", font_size=24).next_to(end1, DOWN, 0.4)
        self.play(FadeIn(end1, shift=UP * 0.3), FadeIn(end2, shift=UP * 0.3))
        self.wait(2)
        self.play(FadeOut(end1), FadeOut(end2))
