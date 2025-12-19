from manim import (
    Scene, Text, MathTex, VGroup, Circle, Dot, RoundedRectangle, SurroundingRectangle,
    FadeIn, FadeOut, Write, Transform, Indicate,
    UP, DOWN, RIGHT, LEFT,
    BLUE, BLUE_E, YELLOW, YELLOW_E, GREEN, GREEN_E, WHITE,
)
import numpy as np


class SuboptimalityGapIntro(Scene):
    """
    Segment: Explain and compute suboptimality gaps Delta_i = mu^* - mu_i
    using the same visual environment as BanditIntro.
    """

    mus = [0.6, 0.2, 0.8, 0.4]   # same as BanditIntro

    def construct(self):
        # ----- Header -----
        header = Text("Suboptimality Gap", font_size=40).to_edge(UP)
        self.play(FadeIn(header))

        # ----- Same arm layout as BanditIntro -----
        x_spacing = 1.7
        radius = 0.4
        dist_label_y_offset = 0.6

        action_circles = VGroup()
        action_labels  = VGroup()
        mean_labels    = VGroup()

        for i, mu in enumerate(self.mus):
            x_shift = RIGHT * x_spacing * (i - (len(self.mus) - 1) / 2)

            circle = (
                Circle(radius=radius)
                .set_fill(BLUE, opacity=0.25)
                .set_stroke(BLUE_E, width=2)
                .shift(x_shift)
            )
            action_circles.add(circle)

            a_label = MathTex(fr"a_{i+1}").scale(0.7).move_to(circle.get_center())
            action_labels.add(a_label)

            # Use mean label instead of Normal dist for this scene
            # (keeps the same "label above/below" vibe)
            direction = UP if (i % 2 == 0) else DOWN
            mu_tex = MathTex(rf"\mu_{i+1} = {mu:.2f}").scale(0.8).next_to(
                circle, direction, buff=dist_label_y_offset
            )
            mean_labels.add(mu_tex)

        self.play(FadeIn(action_circles), Write(action_labels))
        self.play(Write(mean_labels))
        self.wait(0.4)

        # ----- Define mu^* and Delta_i -----
        mu_star = max(self.mus)
        i_star = int(np.argmax(self.mus))  # 0-indexed

        definition = MathTex(
            r"\Delta_i \;:=\; \mu^\* - \mu_i",
            font_size=34
        ).next_to(header, DOWN, buff=0.35)

        mu_star_tex = MathTex(
            rf"\mu^\* = \max_i \mu_i = {mu_star:.2f}",
            font_size=34
        ).next_to(definition, DOWN, buff=0.25)

        self.play(Write(definition))
        self.play(Write(mu_star_tex))
        self.wait(0.6)

        # Highlight the optimal arm (the one attaining mu*)
        optimal_circle = action_circles[i_star]
        optimal_label = action_labels[i_star]

        optimal_tag = Text("optimal arm", font_size=24).next_to(optimal_circle, DOWN, buff=0.9)
        opt_box = SurroundingRectangle(optimal_circle, buff=0.18)

        self.play(
            optimal_circle.animate.set_fill(GREEN, opacity=0.45).set_stroke(GREEN_E, width=3),
            Indicate(optimal_label, scale_factor=1.1),
            FadeIn(optimal_tag),
            Create(opt_box),
            run_time=0.9
        )
        self.wait(0.6)

        # ----- Compute each Delta_i step-by-step -----
        compute_anchor = mu_star_tex.get_center() + DOWN * 1.1
        current_line = None

        for i, mu in enumerate(self.mus):
            circle = action_circles[i]
            a_lab = action_labels[i]

            # visually focus this arm
            self.play(
                circle.animate.set_fill(YELLOW, opacity=0.9).set_stroke(YELLOW_E, width=3),
                Indicate(a_lab, scale_factor=1.08),
                run_time=0.5
            )

            # Step 1: Delta_i = mu* - mu_i
            line1 = MathTex(
                rf"\Delta_{{{i+1}}} = \mu^\* - \mu_{{{i+1}}}",
                font_size=34
            ).move_to(compute_anchor)

            # Step 2: plug numbers
            line2 = MathTex(
                rf"\Delta_{{{i+1}}} = {mu_star:.2f} - {mu:.2f}",
                font_size=34
            ).move_to(compute_anchor)

            # Step 3: final value
            delta = mu_star - mu
            line3 = MathTex(
                rf"\Delta_{{{i+1}}} = {delta:.2f}",
                font_size=34
            ).move_to(compute_anchor)

            # animate the lines
            if current_line is None:
                self.play(Write(line1), run_time=0.7)
            else:
                self.play(Transform(current_line, line1), run_time=0.6)
            current_line = line1

            self.wait(0.35)
            self.play(Transform(current_line, line2), run_time=0.6)
            self.wait(0.35)
            self.play(Transform(current_line, line3), run_time=0.6)
            self.wait(0.55)

            # If this is the optimal arm, emphasize Delta=0 and keep it green
            if i == i_star:
                zero_tag = Text("gap = 0", font_size=22).next_to(circle, UP, buff=0.85)
                self.play(
                    circle.animate.set_fill(GREEN, opacity=0.45).set_stroke(GREEN_E, width=3),
                    FadeIn(zero_tag),
                    Indicate(current_line, scale_factor=1.06),
                    run_time=0.7
                )
                self.wait(0.4)
                self.play(FadeOut(zero_tag), run_time=0.3)
            else:
                # reset non-optimal arms to "visited"-ish green (like BanditIntro),
                # but not as strong as optimal.
                self.play(
                    circle.animate.set_fill(GREEN, opacity=0.30).set_stroke(GREEN_E, width=2),
                    run_time=0.35
                )

            self.wait(0.15)

        self.wait(0.6)

        # ----- Clean exit -----
        self.play(
            FadeOut(current_line),
            FadeOut(opt_box),
            FadeOut(optimal_tag),
            FadeOut(mu_star_tex),
            FadeOut(definition),
            FadeOut(mean_labels),
            FadeOut(action_labels),
            FadeOut(action_circles),
            FadeOut(header),
            run_time=0.8
        )
        self.wait(0.3)
