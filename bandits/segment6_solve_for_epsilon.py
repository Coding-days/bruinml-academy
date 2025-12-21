from manim import *
import numpy as np

#! WORK IN PROGRESS!!!!

class SolveForEpsilon(Scene):
    def construct(self):
        # 1. Header
        header = Text("Solving for ε: Introducing δ", font_size=36).to_edge(UP)
        self.play(FadeIn(header))
        self.wait(0.5)

        # 2. Starting concentration inequality
        conc_bound = MathTex(
            r"\mathbb{P}\left(\hat\mu \geq \mu + \varepsilon\right)",
            r"\leq",
            r"\exp\left(-\frac{n\varepsilon^2}{2\sigma^2}\right)"
        ).shift(UP * 1.5)
        self.play(Write(conc_bound))
        self.wait(1.5)

        # 3. Introduce delta - highlight the RHS
        rhs_box = SurroundingRectangle(conc_bound[2], color=YELLOW, buff=0.1)
        self.play(Create(rhs_box))
        self.wait(0.5)

        # Add explanatory text
        intro_text = Text("Let δ equal this bound", font_size=28, color=YELLOW).next_to(rhs_box, DOWN, buff=0.3)
        self.play(FadeIn(intro_text))
        self.wait(1)

        # Show delta definition
        delta_def = MathTex(
            r"\delta", r"=", r"\exp\left(-\frac{n\varepsilon^2}{2\sigma^2}\right)"
        ).next_to(intro_text, DOWN, buff=0.5)
        delta_def[0].set_color(YELLOW)
        self.play(Write(delta_def))
        self.wait(1.5)

        # Fade out the bound and intro, keep delta definition
        self.play(FadeOut(conc_bound), FadeOut(rhs_box), FadeOut(intro_text))
        self.play(delta_def.animate.move_to(UP * 2))
        self.wait(0.5)

        # 4. Algebraic derivation - Step by step transforms

        # Step 4a: Take natural log
        step_label_a = Text("Take log of both sides:", font_size=24, color=BLUE).next_to(delta_def, DOWN, buff=0.6).to_edge(LEFT, buff=1)
        self.play(FadeIn(step_label_a))

        step_a = MathTex(
            r"\log(\delta)", r"=", r"-\frac{n\varepsilon^2}{2\sigma^2}"
        ).next_to(step_label_a, DOWN, buff=0.3).shift(RIGHT * 0.5)
        step_a[0].set_color(YELLOW)
        self.play(Write(step_a))
        self.wait(1.2)

        # Step 4b: Multiply by -1 / rewrite
        step_label_b = Text("Rewrite:", font_size=24, color=BLUE).next_to(step_a, DOWN, buff=0.5).to_edge(LEFT, buff=1)
        self.play(FadeIn(step_label_b))

        step_b = MathTex(
            r"\log\left(\frac{1}{\delta}\right)", r"=", r"\frac{n\varepsilon^2}{2\sigma^2}"
        ).next_to(step_label_b, DOWN, buff=0.3).shift(RIGHT * 0.5)
        step_b[0].set_color(YELLOW)
        self.play(Write(step_b))
        self.wait(1.2)

        # Step 4c: Isolate epsilon squared
        step_label_c = Text("Isolate ε²:", font_size=24, color=BLUE).next_to(step_b, DOWN, buff=0.5).to_edge(LEFT, buff=1)
        self.play(FadeIn(step_label_c))

        step_c = MathTex(
            r"\varepsilon^2", r"=", r"\frac{2\sigma^2 \log(1/\delta)}{n}"
        ).next_to(step_label_c, DOWN, buff=0.3).shift(RIGHT * 0.5)
        step_c[0].set_color(GREEN)
        self.play(Write(step_c))
        self.wait(1.2)

        # Step 4d: Take square root
        step_label_d = Text("Take square root:", font_size=24, color=BLUE).next_to(step_c, DOWN, buff=0.5).to_edge(LEFT, buff=1)
        self.play(FadeIn(step_label_d))

        step_d = MathTex(
            r"\varepsilon", r"=", r"\sigma\sqrt{\frac{2\log(1/\delta)}{n}}"
        ).next_to(step_label_d, DOWN, buff=0.3).shift(RIGHT * 0.5)
        step_d[0].set_color(GREEN)
        self.play(Write(step_d))
        self.wait(1.5)

        # 5. Final result - fade out intermediate, highlight final
        self.play(
            FadeOut(header),
            FadeOut(delta_def),
            FadeOut(step_label_a), FadeOut(step_a),
            FadeOut(step_label_b), FadeOut(step_b),
            FadeOut(step_label_c), FadeOut(step_c),
            FadeOut(step_label_d)
        )

        # Move final formula to center and scale up
        final_formula = MathTex(
            r"\varepsilon", r"=", r"\sigma\sqrt{\frac{2\log(1/\delta)}{n}}"
        ).scale(1.3)
        final_formula[0].set_color(GREEN)
        self.play(Transform(step_d, final_formula))
        self.wait(0.5)

        # Add box around final result
        final_box = SurroundingRectangle(step_d, color=YELLOW, buff=0.2)
        self.play(Create(final_box))

        # Add label
        result_label = Text("Confidence bound width", font_size=28).next_to(final_box, DOWN, buff=0.4)
        self.play(FadeIn(result_label))
        self.wait(2.5)

        # Final fade out
        self.play(FadeOut(step_d), FadeOut(final_box), FadeOut(result_label))
        self.wait(0.5)
