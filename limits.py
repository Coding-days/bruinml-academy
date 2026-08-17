from manim import *
import numpy as np

class LimitsVideo(Scene):
    def construct(self):
        self.camera.background_color = "#1a1a2e"

        # ── Helper: caption with line-wrap ──
        def caption(text, **kwargs):
            return Text(text, font_size=28, color=YELLOW, **kwargs).to_edge(DOWN, buff=0.4)

        def clear_all(self, *mobjects):
            self.play(*[FadeOut(m) for m in mobjects])

        # ═══════════════════════════════════════
        # SCENE 1: Title
        # ═══════════════════════════════════════
        title = Text("Limits of Sequences\nand Functions", font_size=52, line_spacing=1.3)
        subtitle = Text("An Introduction", font_size=30, color=GREY_B).next_to(title, DOWN, buff=0.5)
        self.play(Write(title), run_time=2)
        self.play(FadeIn(subtitle, shift=UP*0.3))
        self.wait(1.5)
        self.play(FadeOut(title), FadeOut(subtitle))
        self.wait(0.5)

        # ═══════════════════════════════════════
        # SCENE 2: Motivation
        # ═══════════════════════════════════════
        cap1 = caption("Imagine a sequence\nof numbers...")
        seq_tex = MathTex(r"a_1,\; a_2,\; a_3,\; \dots", font_size=48)
        self.play(Write(seq_tex), FadeIn(cap1))
        self.wait(2)

        cap2 = caption("Does this sequence\napproach some value?")
        self.play(ReplacementTransform(cap1, cap2))
        self.wait(2)

        cap3 = caption("That value is\nthe limit.")
        self.play(ReplacementTransform(cap2, cap3))
        self.wait(2)
        self.play(FadeOut(seq_tex), FadeOut(cap3))
        self.wait(0.5)

        # ═══════════════════════════════════════
        # SCENE 3: Epsilon-N definition
        # ═══════════════════════════════════════
        def_title = Text("Definition: Limit of a Sequence", font_size=36, color=BLUE_B)
        def_title.to_edge(UP, buff=0.5)
        self.play(Write(def_title))

        line1 = MathTex(r"\lim_{n \to \infty} a_n = L", font_size=44)
        line1.next_to(def_title, DOWN, buff=0.6)
        self.play(Write(line1))
        self.wait(1)

        cap4 = caption("means: for every\nepsilon > 0 ...")
        line2 = MathTex(
            r"\text{if } \forall\, \epsilon > 0,\;"
            r"\exists\, N \text{ such that}",
            font_size=36
        )
        line2.next_to(line1, DOWN, buff=0.5)
        self.play(Write(line2), FadeIn(cap4))
        self.wait(2)

        line3 = MathTex(
            r"n > N \;\Longrightarrow\; |a_n - L| < \epsilon",
            font_size=42
        )
        line3.next_to(line2, DOWN, buff=0.5)

        cap5 = caption("...all later terms are\nwithin epsilon of L.")
        self.play(ReplacementTransform(cap4, cap5))
        self.play(Write(line3))
        self.wait(3)

        # Highlight key dependency
        cap6 = caption("N is allowed to\ndepend on epsilon.")
        self.play(ReplacementTransform(cap5, cap6))

        box_N = SurroundingRectangle(line2[-1][3:4], color=RED, buff=0.1)
        box_eps = SurroundingRectangle(line2[-1][5:6], color=GREEN, buff=0.1)
        self.play(Create(box_N), Create(box_eps))
        self.wait(2.5)
        self.play(
            FadeOut(def_title), FadeOut(line1), FadeOut(line2),
            FadeOut(line3), FadeOut(box_N), FadeOut(box_eps), FadeOut(cap6)
        )
        self.wait(0.5)

        # ═══════════════════════════════════════
        # SCENE 4: Intuition paragraph
        # ═══════════════════════════════════════
        intuition_lines = [
            Text("No matter how small", font_size=30),
            Text("a tolerance ε you pick,", font_size=30),
            Text("you can go far enough", font_size=30),
            Text("out in the sequence", font_size=30),
            Text("so all later terms", font_size=30),
            Text("lie within ε of L.", font_size=30),
        ]
        intuition_group = VGroup(*intuition_lines).arrange(DOWN, buff=0.2).move_to(ORIGIN)
        for line in intuition_lines:
            self.play(FadeIn(line, shift=RIGHT*0.3), run_time=0.6)
        self.wait(3)
        self.play(FadeOut(intuition_group))
        self.wait(0.5)

        # ═══════════════════════════════════════
        # SCENE 5: Example a_n = 1/n (detailed)
        # ═══════════════════════════════════════
        ex_title = Text("Example", font_size=36, color=GREEN_B).to_edge(UP, buff=0.5)
        ex_seq = MathTex(r"a_n = \frac{1}{n}", font_size=44).next_to(ex_title, DOWN, buff=0.35)
        ex_claim = MathTex(r"\text{Prove: } \lim_{n\to\infty} a_n = 0", font_size=38).next_to(ex_seq, DOWN, buff=0.25)
        self.play(Write(ex_title))
        self.play(Write(ex_seq))
        self.play(Write(ex_claim))
        self.wait(1)

        # Step 1: Let epsilon > 0
        cap7a = caption("Let ε > 0 be given.")
        pf_let = MathTex(
            r"\text{Let } \epsilon > 0 \text{ be given.}",
            font_size=34
        ).next_to(ex_claim, DOWN, buff=0.45)
        self.play(FadeIn(cap7a), Write(pf_let))
        self.wait(1.5)

        # Step 2: Choose N
        cap7b = caption("Choose N > 1/ε.")
        pf_choose = MathTex(
            r"\text{Choose } N > \frac{1}{\epsilon}.",
            font_size=34
        ).next_to(pf_let, DOWN, buff=0.3)
        self.play(ReplacementTransform(cap7a, cap7b), Write(pf_choose))
        self.wait(2)

        # Step 3: Show the implication chain
        cap8 = caption("Then for any n > N\nwe have:")
        pf_impl_header = MathTex(
            r"\text{Then } n > N \;\Longrightarrow",
            font_size=34
        ).next_to(pf_choose, DOWN, buff=0.35)
        self.play(ReplacementTransform(cap7b, cap8), Write(pf_impl_header))
        self.wait(1)

        pf_chain = MathTex(
            r"|a_n - 0|",
            r"= \left|\frac{1}{n}\right|",
            r"= \frac{1}{n}",
            r"\le \frac{1}{N}",
            r"< \epsilon",
            font_size=34
        ).next_to(pf_impl_header, DOWN, buff=0.3)

        # Animate the chain step by step
        self.play(Write(pf_chain[0]))
        self.wait(0.5)
        self.play(Write(pf_chain[1]))
        self.wait(0.5)
        self.play(Write(pf_chain[2]))
        self.wait(0.5)

        cap8b = caption("Since n > N,\nwe have 1/n ≤ 1/N.")
        self.play(ReplacementTransform(cap8, cap8b))
        self.play(Write(pf_chain[3]))
        self.wait(1)

        cap8c = caption("And N > 1/ε means\n1/N < ε.")
        self.play(ReplacementTransform(cap8b, cap8c))
        self.play(Write(pf_chain[4]))
        self.wait(2)

        # Conclusion
        cap9 = caption("So the limit\nis indeed 0.  ∎")
        self.play(ReplacementTransform(cap8c, cap9))
        self.wait(2)
        self.play(
            FadeOut(ex_title), FadeOut(ex_seq), FadeOut(ex_claim),
            FadeOut(pf_let), FadeOut(pf_choose),
            FadeOut(pf_impl_header), FadeOut(pf_chain), FadeOut(cap9)
        )
        self.wait(0.5)

        # ═══════════════════════════════════════
        # SCENE 6: Graph of a_n = 1/n
        # ═══════════════════════════════════════
        graph_title = Text("Visualizing the Limit", font_size=36, color=BLUE_B).to_edge(UP, buff=0.4)
        self.play(Write(graph_title))

        axes = Axes(
            x_range=[0, 21, 2],
            y_range=[-0.15, 1.1, 0.2],
            x_length=10,
            y_length=5,
            axis_config={"include_numbers": False, "tip_width": 0.15, "tip_height": 0.15},
        ).shift(DOWN*0.3)

        x_labels = VGroup()
        for val in [2, 6, 10, 14, 18, 20]:
            lab = MathTex(str(val), font_size=22).next_to(axes.c2p(val, 0), DOWN, buff=0.15)
            x_labels.add(lab)

        y_labels = VGroup()
        for val, txt in [(0.2, r"\epsilon"), (0.5, "0.5"), (1.0, "1")]:
            lab = MathTex(txt, font_size=22).next_to(axes.c2p(0, val), LEFT, buff=0.15)
            y_labels.add(lab)

        n_label = MathTex("n", font_size=26).next_to(axes.c2p(21, 0), RIGHT, buff=0.1)
        a_label = MathTex("a_n", font_size=26).next_to(axes.c2p(0, 1.1), UP, buff=0.1)

        self.play(Create(axes), FadeIn(x_labels), FadeIn(y_labels), FadeIn(n_label), FadeIn(a_label))

        # Epsilon band
        eps_val = 0.2
        eps_band = Polygon(
            axes.c2p(0, -eps_val), axes.c2p(21, -eps_val),
            axes.c2p(21, eps_val), axes.c2p(0, eps_val),
            fill_color=BLUE, fill_opacity=0.15, stroke_width=0
        )
        eps_line = DashedLine(
            axes.c2p(0, eps_val), axes.c2p(21, eps_val),
            color=BLUE, dash_length=0.1
        )
        limit_line = Line(axes.c2p(0, 0), axes.c2p(21, 0), color=WHITE, stroke_width=2)

        cap10 = caption("The blue band is\nthe ε-neighborhood.")
        self.play(FadeIn(eps_band), Create(eps_line), Create(limit_line), FadeIn(cap10))
        self.wait(1.5)

        # Plot dots before N
        dots_before = VGroup()
        for n in range(1, 7):
            dot = Dot(axes.c2p(n, 1/n), radius=0.05, color=WHITE)
            dots_before.add(dot)

        cap11 = caption("Terms before N = 6\nmay be outside.")
        self.play(ReplacementTransform(cap10, cap11))
        self.play(LaggedStart(*[FadeIn(d, scale=0.5) for d in dots_before], lag_ratio=0.15))
        self.wait(1.5)

        # Cutoff line
        cutoff = DashedLine(
            axes.c2p(6, -0.12), axes.c2p(6, 1.05),
            color=RED, stroke_width=2.5, dash_length=0.08
        )
        n_label_cutoff = MathTex(r"N=6", font_size=24, color=RED).next_to(axes.c2p(6, -0.12), DOWN, buff=0.15)
        self.play(Create(cutoff), FadeIn(n_label_cutoff))
        self.wait(1)

        # Dots after N
        dots_after = VGroup()
        for n in range(7, 21):
            dot = Dot(axes.c2p(n, 1/n), radius=0.05, color=BLUE)
            dots_after.add(dot)

        cap12 = caption("All terms after N\nstay inside the band!")
        self.play(ReplacementTransform(cap11, cap12))
        self.play(LaggedStart(*[FadeIn(d, scale=0.5) for d in dots_after], lag_ratio=0.1))
        self.wait(1)

        annotation = MathTex(
            r"|a_n - 0| < \epsilon \text{ for all } n > N",
            font_size=26, color=BLUE_B
        ).next_to(axes.c2p(14, 0.2), UP, buff=0.2)
        self.play(FadeIn(annotation))
        self.wait(3)

        # Clear graph
        graph_group = VGroup(
            graph_title, axes, x_labels, y_labels, n_label, a_label,
            eps_band, eps_line, limit_line, dots_before, dots_after,
            cutoff, n_label_cutoff, annotation, cap12
        )
        self.play(FadeOut(graph_group))
        self.wait(0.5)

        # ═══════════════════════════════════════
        # SCENE 7: Key takeaway about N depending on epsilon
        # ═══════════════════════════════════════
        takeaway = VGroup(
            Text("Key Point:", font_size=34, color=YELLOW),
            Text("Smaller ε means", font_size=30),
            Text("larger N needed.", font_size=30),
        ).arrange(DOWN, buff=0.3).move_to(ORIGIN)
        self.play(FadeIn(takeaway, shift=UP*0.3))
        self.wait(3)
        self.play(FadeOut(takeaway))
        self.wait(0.5)

        # ═══════════════════════════════════════
        # SCENE 8: Transition to function limits
        # ═══════════════════════════════════════
        trans_text = Text(
            "Now: Limits of Functions",
            font_size=42, color=TEAL_B
        )
        self.play(Write(trans_text))
        self.wait(2)
        self.play(FadeOut(trans_text))
        self.wait(0.5)

        # ═══════════════════════════════════════
        # SCENE 9: Epsilon-delta definition
        # ═══════════════════════════════════════
        def2_title = Text("Definition: Limit of a Function", font_size=36, color=BLUE_B)
        def2_title.to_edge(UP, buff=0.5)
        self.play(Write(def2_title))

        func_lim = MathTex(r"\lim_{x \to a} f(x) = L", font_size=44)
        func_lim.next_to(def2_title, DOWN, buff=0.5)
        self.play(Write(func_lim))
        self.wait(1)

        cap13 = caption("For every ε > 0,\nthere exists δ > 0...")
        cond = MathTex(
            r"\forall\, \epsilon > 0,\;\exists\, \delta > 0 \text{ such that}",
            font_size=36
        ).next_to(func_lim, DOWN, buff=0.4)
        self.play(FadeIn(cap13), Write(cond))
        self.wait(2)

        impl = MathTex(
            r"0 < |x - a| < \delta \;\Longrightarrow\; |f(x) - L| < \epsilon",
            font_size=38
        ).next_to(cond, DOWN, buff=0.4)

        cap14 = caption("...inputs near a give\noutputs near L.")
        self.play(ReplacementTransform(cap13, cap14), Write(impl))
        self.wait(3)

        self.play(
            FadeOut(def2_title), FadeOut(func_lim),
            FadeOut(cond), FadeOut(impl), FadeOut(cap14)
        )
        self.wait(0.5)

        # ═══════════════════════════════════════
        # SCENE 10: Comparing the two definitions
        # ═══════════════════════════════════════
        comp_title = Text("Comparing the Two Definitions", font_size=34, color=TEAL_B).to_edge(UP, buff=0.5)
        self.play(Write(comp_title))

        seq_box = VGroup(
            Text("Sequence Limit", font_size=26, color=GREEN_B),
            MathTex(r"\epsilon\text{-}N", font_size=34),
            MathTex(r"n > N", font_size=28),
            MathTex(r"|a_n - L| < \epsilon", font_size=28),
        ).arrange(DOWN, buff=0.25)
        seq_rect = SurroundingRectangle(seq_box, color=GREEN, buff=0.3)
        seq_group = VGroup(seq_rect, seq_box).shift(LEFT*3 + DOWN*0.3)

        func_box = VGroup(
            Text("Function Limit", font_size=26, color=BLUE_B),
            MathTex(r"\epsilon\text{-}\delta", font_size=34),
            MathTex(r"0 < |x-a| < \delta", font_size=28),
            MathTex(r"|f(x) - L| < \epsilon", font_size=28),
        ).arrange(DOWN, buff=0.25)
        func_rect = SurroundingRectangle(func_box, color=BLUE, buff=0.3)
        func_group = VGroup(func_rect, func_box).shift(RIGHT*3 + DOWN*0.3)

        arrow = Arrow(seq_group.get_right(), func_group.get_left(), buff=0.2, color=GREY_B)
        arr_label = Text("same idea!", font_size=22, color=GREY_B).next_to(arrow, UP, buff=0.1)

        cap15 = caption("Index N becomes\nradius δ.")
        self.play(FadeIn(seq_group), FadeIn(cap15))
        self.wait(1.5)
        self.play(FadeIn(func_group), GrowArrow(arrow), FadeIn(arr_label))
        self.wait(3)

        self.play(
            FadeOut(comp_title), FadeOut(seq_group), FadeOut(func_group),
            FadeOut(arrow), FadeOut(arr_label), FadeOut(cap15)
        )
        self.wait(0.5)

        # ═══════════════════════════════════════
        # SCENE 11: Continuity definition
        # ═══════════════════════════════════════
        cont_title = Text("Continuity", font_size=36, color=BLUE_B).to_edge(UP, buff=0.5)
        self.play(Write(cont_title))

        cont_def = MathTex(
            r"f \text{ is continuous at } x = a \;\text{ if }\;"
            r"\lim_{x \to a} f(x) = f(a)",
            font_size=36
        ).next_to(cont_title, DOWN, buff=0.6)
        self.play(Write(cont_def))

        cap16 = caption("The limit equals\nthe function value.")
        self.play(FadeIn(cap16))
        self.wait(3)

        self.play(FadeOut(cont_title), FadeOut(cont_def), FadeOut(cap16))
        self.wait(0.5)

        # ═══════════════════════════════════════
        # SCENE 12: Example f(x) = x^2, lim x->2
        # ═══════════════════════════════════════
        ex2_title = Text("Example", font_size=36, color=GREEN_B).to_edge(UP, buff=0.5)
        ex2_claim = MathTex(
            r"\text{Prove: } \lim_{x\to 2} x^2 = 4",
            font_size=42
        ).next_to(ex2_title, DOWN, buff=0.5)
        self.play(Write(ex2_title), Write(ex2_claim))
        self.wait(2)

        # Scratch work
        cap17 = caption("Factor the\ndifference first.")
        scratch1 = MathTex(
            r"|x^2 - 4| = |x-2|\,|x+2|",
            font_size=38
        ).next_to(ex2_claim, DOWN, buff=0.6)
        self.play(FadeIn(cap17), Write(scratch1))
        self.wait(2.5)

        cap18 = caption("If |x − 2| < 1,\nthen |x + 2| ≤ 5.")
        scratch2 = MathTex(
            r"|x-2| < 1 \;\Longrightarrow\; |x+2| \le 5",
            font_size=36
        ).next_to(scratch1, DOWN, buff=0.4)
        self.play(ReplacementTransform(cap17, cap18), Write(scratch2))
        self.wait(2.5)

        cap19 = caption("So |x² − 4| ≤ 5|x − 2|.")
        scratch3 = MathTex(
            r"|x^2 - 4| \le 5|x-2|",
            font_size=36
        ).next_to(scratch2, DOWN, buff=0.4)
        self.play(ReplacementTransform(cap18, cap19), Write(scratch3))
        self.wait(2)

        self.play(
            FadeOut(scratch1), FadeOut(scratch2), FadeOut(scratch3), FadeOut(cap19)
        )
        self.wait(0.3)

        # Choosing delta
        cap20 = caption("Choose δ = min{1, ε/5}.")
        delta_choice = MathTex(
            r"\delta := \min\!\left\{1,\; \frac{\epsilon}{5}\right\}",
            font_size=42
        ).next_to(ex2_claim, DOWN, buff=0.6)
        self.play(FadeIn(cap20), Write(delta_choice))
        self.wait(2.5)

        # Final chain
        cap21 = caption("Then the bound\ngives us ε.")
        chain = MathTex(
            r"|x^2-4| \le 5|x-2| < 5 \cdot \frac{\epsilon}{5} = \epsilon",
            font_size=36
        ).next_to(delta_choice, DOWN, buff=0.5)
        self.play(ReplacementTransform(cap20, cap21), Write(chain))
        self.wait(3)

        cap22 = caption("Therefore the limit\nis 4.  ∎")
        self.play(ReplacementTransform(cap21, cap22))
        self.wait(2)

        self.play(
            FadeOut(ex2_title), FadeOut(ex2_claim),
            FadeOut(delta_choice), FadeOut(chain), FadeOut(cap22)
        )
        self.wait(0.3)

        # ── Continuity remark ──
        cont_remark_title = Text("Continuity at x = 2", font_size=34, color=TEAL_B).to_edge(UP, buff=0.6)
        self.play(Write(cont_remark_title))

        cont_r1 = MathTex(
            r"\lim_{x \to 2} x^2 = 4",
            font_size=40
        ).next_to(cont_remark_title, DOWN, buff=0.5)
        cont_r2 = MathTex(
            r"f(2) = 2^2 = 4",
            font_size=40
        ).next_to(cont_r1, DOWN, buff=0.4)
        self.play(Write(cont_r1))
        self.wait(1)
        self.play(Write(cont_r2))
        self.wait(1)

        cap_cont = caption("Limit equals f(2),\nso f is continuous there.")
        cont_r3 = MathTex(
            r"\lim_{x \to 2} f(x) = f(2)",
            r"\;\Longrightarrow\;",
            r"f \text{ is continuous at } x=2",
            font_size=34
        ).next_to(cont_r2, DOWN, buff=0.5)
        self.play(FadeIn(cap_cont), Write(cont_r3))
        self.wait(3)
        self.play(
            FadeOut(cont_remark_title), FadeOut(cont_r1),
            FadeOut(cont_r2), FadeOut(cont_r3), FadeOut(cap_cont)
        )
        self.wait(0.5)

        # ═══════════════════════════════════════
        # SCENE 13: Epsilon-delta graph for x^2
        # ═══════════════════════════════════════
        g_title = Text("Epsilon-Delta Visualization", font_size=34, color=BLUE_B).to_edge(UP, buff=0.4)
        self.play(Write(g_title))

        axes2 = Axes(
            x_range=[0.5, 3.5, 0.5],
            y_range=[0, 9, 1],
            x_length=9,
            y_length=5.5,
            axis_config={"include_numbers": False, "tip_width": 0.15, "tip_height": 0.15},
        ).shift(DOWN*0.4)

        x2_labels = VGroup()
        for val, txt in [(1, "1"), (1.8, r"2{-}\delta"), (2, "2"), (2.2, r"2{+}\delta"), (3, "3")]:
            lab = MathTex(txt, font_size=20).next_to(axes2.c2p(val, 0), DOWN, buff=0.15)
            x2_labels.add(lab)

        y2_labels = VGroup()
        for val, txt in [(3, r"4{-}\epsilon"), (4, "4"), (5, r"4{+}\epsilon"), (9, "9")]:
            lab = MathTex(txt, font_size=20).next_to(axes2.c2p(0.5, val), LEFT, buff=0.15)
            y2_labels.add(lab)

        x2_ax_label = MathTex("x", font_size=24).next_to(axes2.c2p(3.5, 0), RIGHT, buff=0.1)
        y2_ax_label = MathTex("f(x)", font_size=24).next_to(axes2.c2p(0.5, 9), UP, buff=0.1)

        self.play(Create(axes2), FadeIn(x2_labels), FadeIn(y2_labels), FadeIn(x2_ax_label), FadeIn(y2_ax_label))

        # Epsilon band (horizontal)
        eps_band2 = Polygon(
            axes2.c2p(0.5, 3), axes2.c2p(3.5, 3),
            axes2.c2p(3.5, 5), axes2.c2p(0.5, 5),
            fill_color=BLUE, fill_opacity=0.15, stroke_width=0
        )
        eps_top = DashedLine(axes2.c2p(0.5, 5), axes2.c2p(3.5, 5), color=BLUE, dash_length=0.08)
        eps_bot = DashedLine(axes2.c2p(0.5, 3), axes2.c2p(3.5, 3), color=BLUE, dash_length=0.08)
        l_line = DashedLine(axes2.c2p(0.5, 4), axes2.c2p(3.5, 4), color=WHITE, stroke_width=1.5, dash_length=0.06)

        cap23 = caption("Blue band:\n|f(x) − 4| < ε.")
        self.play(FadeIn(eps_band2), Create(eps_top), Create(eps_bot), Create(l_line), FadeIn(cap23))
        self.wait(1.5)

        # Delta strip (vertical)
        delta_strip = Polygon(
            axes2.c2p(1.8, 0), axes2.c2p(2.2, 0),
            axes2.c2p(2.2, 9), axes2.c2p(1.8, 9),
            fill_color=RED, fill_opacity=0.12, stroke_width=0
        )
        d_left = DashedLine(axes2.c2p(1.8, 0), axes2.c2p(1.8, 9), color=RED, dash_length=0.08)
        d_right = DashedLine(axes2.c2p(2.2, 0), axes2.c2p(2.2, 9), color=RED, dash_length=0.08)

        cap24 = caption("Red strip:\n0 < |x − 2| < δ.")
        self.play(
            ReplacementTransform(cap23, cap24),
            FadeIn(delta_strip), Create(d_left), Create(d_right)
        )
        self.wait(1.5)

        # Parabola
        parabola = axes2.plot(lambda x: x**2, x_range=[0.5, 3.2], color=WHITE, stroke_width=2.5)
        parabola_label = MathTex(r"f(x) = x^2", font_size=24).next_to(axes2.c2p(3.1, 9), LEFT, buff=0.2)

        # Highlighted portion
        parabola_highlight = axes2.plot(
            lambda x: x**2, x_range=[1.8, 2.2],
            color=YELLOW, stroke_width=4
        )

        cap25 = caption("Inside the strip,\nthe curve stays in the band!")
        self.play(
            ReplacementTransform(cap24, cap25),
            Create(parabola), FadeIn(parabola_label)
        )
        self.wait(1)
        self.play(Create(parabola_highlight))

        # Point (2,4)
        pt = Dot(axes2.c2p(2, 4), radius=0.06, color=YELLOW)
        pt_label = MathTex(r"(2,4)", font_size=22).next_to(pt, UR, buff=0.1)
        self.play(FadeIn(pt), FadeIn(pt_label))
        self.wait(3)

        graph2_group = VGroup(
            g_title, axes2, x2_labels, y2_labels, x2_ax_label, y2_ax_label,
            eps_band2, eps_top, eps_bot, l_line,
            delta_strip, d_left, d_right,
            parabola, parabola_label, parabola_highlight,
            pt, pt_label, cap25
        )
        self.play(FadeOut(graph2_group))
        self.wait(0.5)

        # ═══════════════════════════════════════
        # ADDENDUM: When a Limit Does Not Exist
        # ═══════════════════════════════════════
        add_label = Text("Addendum", font_size=28, color=GREY_B).to_corner(UL, buff=0.3)
        dne_title = Text("When a Limit Does Not Exist", font_size=34, color=RED_B).to_edge(UP, buff=0.5)
        self.play(FadeIn(add_label), Write(dne_title))
        self.wait(1)

        # ── Start with the ORIGINAL definition ──
        cap_neg0 = caption("Start with the\noriginal definition.")
        orig_def = MathTex(
            r"\forall\, \epsilon > 0,",          # 0
            r"\;\exists\, \delta > 0",            # 1
            r"\text{ s.t. }",                     # 2
            r"0 < |x-a| < \delta",                # 3
            r"\;\Rightarrow\;",                   # 4
            r"|f(x)-L| < \epsilon",               # 5
            font_size=30
        ).next_to(dne_title, DOWN, buff=0.55)
        self.play(Write(orig_def), FadeIn(cap_neg0))
        self.wait(2)

        # ── Remind: negation swaps quantifiers ──
        cap_rule = caption("Negation rule:\n∀ becomes ∃, ∃ becomes ∀.")
        self.play(ReplacementTransform(cap_neg0, cap_rule))
        self.wait(2)

        # Animate flipping ∀ε → ∃ε
        cap_flip1 = caption("∀ ε becomes ∃ ε₀.")
        new_q1 = MathTex(
            r"\exists\, \epsilon_0 > 0,",
            font_size=30, color=RED
        ).move_to(orig_def[0], aligned_edge=LEFT)
        self.play(
            ReplacementTransform(cap_rule, cap_flip1),
            ReplacementTransform(orig_def[0], new_q1)
        )
        self.wait(1.5)

        # Animate flipping ∃δ → ∀δ
        cap_flip2 = caption("∃ δ becomes ∀ δ.")
        new_q2 = MathTex(
            r"\;\forall\, \delta > 0,",
            font_size=30, color=RED
        ).move_to(orig_def[1], aligned_edge=LEFT)
        self.play(
            ReplacementTransform(cap_flip1, cap_flip2),
            ReplacementTransform(orig_def[1], new_q2)
        )
        self.wait(1.5)

        # Flip ⟹ to "and", flip < to ≥
        cap_flip3 = caption("The implication flips:\n⟹ becomes 'and ... ≥'.")
        new_mid = MathTex(
            r"\text{ s.t. }",
            r"\exists\, x,\;",
            r"0 < |x-a| < \delta",
            r"\;\text{ and }\;",
            r"|f(x)-L| \ge \epsilon_0",
            font_size=30
        )
        # Position to match remaining parts
        remaining_group = VGroup(orig_def[2], orig_def[3], orig_def[4], orig_def[5])
        new_mid.move_to(remaining_group, aligned_edge=LEFT)
        self.play(
            ReplacementTransform(cap_flip2, cap_flip3),
            FadeOut(orig_def[2]), FadeOut(orig_def[3]),
            FadeOut(orig_def[4]), FadeOut(orig_def[5]),
            FadeIn(new_mid)
        )
        self.wait(3)

        # Show the full negation cleanly
        cap_neg_full = caption("This is what we\nmust show.")
        full_neg = MathTex(
            r"\exists\, \epsilon_0 > 0,\;"
            r"\forall\, \delta > 0,\;"
            r"\exists\, x:",
            font_size=30, color=YELLOW
        ).next_to(dne_title, DOWN, buff=0.55)
        full_neg2 = MathTex(
            r"0 < |x-a| < \delta"
            r"\;\text{ and }\;"
            r"|f(x)-L| \ge \epsilon_0",
            font_size=30, color=YELLOW
        ).next_to(full_neg, DOWN, buff=0.25)
        self.play(
            ReplacementTransform(cap_flip3, cap_neg_full),
            FadeOut(new_q1), FadeOut(new_q2), FadeOut(new_mid),
            FadeIn(full_neg), FadeIn(full_neg2)
        )
        self.wait(3)
        self.play(FadeOut(full_neg), FadeOut(full_neg2), FadeOut(cap_neg_full))
        self.wait(0.3)

        # ── Concrete example: sign function ──
        dne_func = MathTex(
            r"f(x) = \begin{cases} 1, & x > 0 \\ -1, & x < 0 \end{cases}",
            font_size=36
        ).next_to(dne_title, DOWN, buff=0.45)
        cap_ex0 = caption("Show: this limit\ndoes not exist at 0.")
        self.play(Write(dne_func), FadeIn(cap_ex0))
        self.wait(2)

        # Graph
        dne_axes = Axes(
            x_range=[-3, 3, 1],
            y_range=[-2, 2, 1],
            x_length=6,
            y_length=2.5,
            axis_config={"include_numbers": True, "font_size": 20, "tip_width": 0.1, "tip_height": 0.1},
        ).shift(DOWN*1.7)

        pos_line_dne = dne_axes.plot(lambda x: 1, x_range=[0.01, 3], color=BLUE)
        neg_line_dne = dne_axes.plot(lambda x: -1, x_range=[-3, -0.01], color=BLUE)
        open_dot_top = Circle(radius=0.07, color=BLUE, stroke_width=2).move_to(dne_axes.c2p(0, 1))
        open_dot_bot = Circle(radius=0.07, color=BLUE, stroke_width=2).move_to(dne_axes.c2p(0, -1))

        cap_ex1 = caption("The graph jumps\nat x = 0.")
        self.play(
            ReplacementTransform(cap_ex0, cap_ex1),
        )
        self.play(
            Create(dne_axes), Create(pos_line_dne), Create(neg_line_dne),
            FadeIn(open_dot_top), FadeIn(open_dot_bot),
        )
        self.wait(1.5)

        # Rigorous proof
        # Step 1: Suppose for contradiction lim = L
        cap_s1 = caption("Suppose for contradiction\nthe limit is L.")
        pf1 = MathTex(
            r"\text{Suppose } \lim_{x\to 0} f(x) = L.",
            font_size=30
        ).next_to(dne_func, DOWN, buff=0.35)
        self.play(ReplacementTransform(cap_ex1, cap_s1), Write(pf1))
        self.wait(2)

        # Step 2: Choose epsilon_0 = 1/2
        # Clear graph to make room for algebra
        self.play(
            FadeOut(dne_axes), FadeOut(pos_line_dne), FadeOut(neg_line_dne),
            FadeOut(open_dot_top), FadeOut(open_dot_bot),
        )

        cap_s2 = caption("Choose ε₀ = 1/2.")
        pf2 = MathTex(
            r"\text{Take } \epsilon_0 = \tfrac{1}{2}.",
            font_size=30
        ).next_to(pf1, DOWN, buff=0.3)
        self.play(ReplacementTransform(cap_s1, cap_s2), Write(pf2))
        self.wait(1.5)

        # Step 3: For any delta, pick two witnesses
        cap_s3 = caption("For any δ > 0, pick\nx₁ = δ/2 and x₂ = −δ/2.")
        pf3 = MathTex(
            r"\text{Let } \delta > 0."
            r"\text{ Set } x_1 = \tfrac{\delta}{2},\;"
            r"x_2 = -\tfrac{\delta}{2}.",
            font_size=28
        ).next_to(pf2, DOWN, buff=0.3)
        self.play(ReplacementTransform(cap_s2, cap_s3), Write(pf3))
        self.wait(2)

        # Step 4: Both are in the delta-ball
        cap_s4 = caption("Both satisfy\n0 < |xᵢ| < δ.")
        pf4 = MathTex(
            r"0 < |x_1| = \tfrac{\delta}{2} < \delta,"
            r"\quad"
            r"0 < |x_2| = \tfrac{\delta}{2} < \delta",
            font_size=26
        ).next_to(pf3, DOWN, buff=0.3)
        self.play(ReplacementTransform(cap_s3, cap_s4), Write(pf4))
        self.wait(2)

        # Step 5: Triangle inequality
        self.play(FadeOut(pf1), FadeOut(pf2))
        pf3.generate_target()
        pf3.target.next_to(dne_func, DOWN, buff=0.35)
        pf4.generate_target()
        pf4.target.next_to(pf3.target, DOWN, buff=0.3)
        self.play(MoveToTarget(pf3), MoveToTarget(pf4))

        cap_s5 = caption("By the triangle\ninequality:")
        pf5 = MathTex(
            r"|f(x_1) - f(x_2)|",
            r"\le |f(x_1) - L|",
            r"+ |f(x_2) - L|",
            font_size=28
        ).next_to(pf4, DOWN, buff=0.3)
        self.play(ReplacementTransform(cap_s4, cap_s5), Write(pf5))
        self.wait(2)

        # Step 6: But f(x1) - f(x2) = 1 - (-1) = 2
        cap_s6 = caption("But f(x₁) − f(x₂)\n= 1 − (−1) = 2.")
        pf6 = MathTex(
            r"|f(x_1) - f(x_2)| = |1 - (-1)| = 2",
            font_size=28
        ).next_to(pf5, DOWN, buff=0.3)
        self.play(ReplacementTransform(cap_s5, cap_s6), Write(pf6))
        self.wait(2)

        # Step 7: So at least one of them >= 1
        cap_s7 = caption("So at least one of\n|f(xᵢ) − L| ≥ 1.")
        pf7 = MathTex(
            r"\therefore\;"
            r"\max\!\big(|f(x_1)-L|,\,|f(x_2)-L|\big)"
            r"\ge 1"
            r"> \tfrac{1}{2} = \epsilon_0",
            font_size=26
        ).next_to(pf6, DOWN, buff=0.3)
        self.play(ReplacementTransform(cap_s6, cap_s7), Write(pf7))
        self.wait(3)

        # Conclusion
        cap_s8 = caption("Contradiction.\nThe limit does not exist.")
        conc = MathTex(
            r"\Longrightarrow\;\lim_{x\to 0} f(x) \text{ does not exist.}",
            font_size=32, color=RED
        ).next_to(pf7, DOWN, buff=0.35)
        self.play(ReplacementTransform(cap_s7, cap_s8), Write(conc))
        self.wait(3)

        self.play(
            FadeOut(add_label), FadeOut(dne_title), FadeOut(dne_func),
            FadeOut(pf3), FadeOut(pf4), FadeOut(pf5),
            FadeOut(pf6), FadeOut(pf7), FadeOut(conc), FadeOut(cap_s8)
        )
        self.wait(0.5)

        # ═══════════════════════════════════════
        # SCENE 16: Summary
        # ═══════════════════════════════════════
        summary_title = Text("Summary", font_size=42, color=YELLOW).to_edge(UP, buff=0.8)
        self.play(Write(summary_title))

        s1 = VGroup(
            MathTex(r"\epsilon\text{-}N", font_size=36, color=GREEN_B),
            Text(": sequence limits", font_size=28),
        ).arrange(RIGHT, buff=0.2)

        s2 = VGroup(
            MathTex(r"\epsilon\text{-}\delta", font_size=36, color=BLUE_B),
            Text(": function limits", font_size=28),
        ).arrange(RIGHT, buff=0.2)

        s3 = Text("Continuity: limit = value", font_size=28, color=TEAL_B)

        summary_group = VGroup(s1, s2, s3).arrange(DOWN, buff=0.5).next_to(summary_title, DOWN, buff=0.8)

        for item in [s1, s2, s3]:
            self.play(FadeIn(item, shift=RIGHT*0.3))
            self.wait(1)

        self.wait(3)
        self.play(FadeOut(summary_title), FadeOut(summary_group))
        self.wait(1)
