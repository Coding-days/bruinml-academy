from shared import *

class BanditIntro(Scene):
    """
    Segment 1: Bandit arms + distributions + random pulls (with reward popups).
    """

    mus     = [0.6, 0.2, 0.8, 0.4]
    sigmas  = [0.15, 0.1, 0.2, 0.12]
    n_pulls = 5

    def construct(self):
        np.random.seed(SEED_PULLS)

        header = Text("Bandit Arms and Reward Means", font_size=36).to_edge(UP)
        self.play(FadeIn(header))

        x_spacing = 1.7
        radius = 0.4
        dist_label_y_offset = 0.6

        action_circles = VGroup()
        action_labels  = VGroup()
        dist_labels    = VGroup()

        for i, (mu, sigma) in enumerate(zip(self.mus, self.sigmas)):
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

            direction = UP if (i % 2 == 0) else DOWN
            dist_tex = MathTex(
                r"\mathcal{N}\!\left(" + f"{mu:.2f}" + r",\, " + f"{sigma:.2f}" + r"\right)"
            ).scale(0.8).next_to(circle, direction, buff=dist_label_y_offset)
            dist_labels.add(dist_tex)

        self.play(FadeIn(action_circles), Write(action_labels))
        self.play(Write(dist_labels))
        self.wait(0.4)

        legend = VGroup(
            Dot().set_fill(YELLOW, opacity=0.9), Text("pull highlight", font_size=22),
            Dot().set_fill(GREEN,  opacity=0.35), Text("visited", font_size=22),
        ).arrange(RIGHT, buff=0.3).to_edge(DOWN)
        self.play(FadeIn(legend))

        pulls = np.random.randint(0, len(self.mus), size=self.n_pulls)

        for t, arm_idx in enumerate(pulls, start=1):
            circle = action_circles[arm_idx]
            center = circle.get_center()

            self.play(
                circle.animate.set_fill(YELLOW, opacity=0.9).set_stroke(YELLOW_E, width=3),
                run_time=0.3
            )

            reward = np.random.normal(self.mus[arm_idx], self.sigmas[arm_idx])
            reward_text = DecimalNumber(reward, num_decimal_places=3).scale(0.7)
            reward_text.move_to(center + UP * 1.0)

            bubble = (
                RoundedRectangle(corner_radius=0.1, width=2.1, height=0.6)
                .set_fill(WHITE, opacity=0.15)
                .set_stroke(WHITE, opacity=0.4, width=1)
                .move_to(reward_text.get_center())
            )

            pull_label = Text(f"Pull {t}: a_{arm_idx+1}", font_size=26).next_to(header, DOWN)

            self.play(
                FadeIn(bubble, scale=0.9),
                FadeIn(reward_text, shift=UP * 0.2),
                FadeTransformPieces(header.copy(), pull_label),
                run_time=0.4
            )
            self.wait(0.2)

            self.play(
                reward_text.animate.shift(UP * 0.5),
                bubble.animate.shift(UP * 0.5).set_opacity(0.05),
                rate_func=smooth,
                run_time=0.35
            )
            self.play(FadeOut(reward_text), FadeOut(bubble), FadeOut(pull_label), run_time=0.25)

            self.play(
                circle.animate.set_fill(GREEN, opacity=0.35).set_stroke(GREEN_E, width=2),
                run_time=0.2
            )
            self.wait(0.05)

        self.play(
            FadeOut(legend),
            FadeOut(dist_labels),
            FadeOut(action_labels),
            FadeOut(action_circles),
            FadeOut(header),
            run_time=0.6
        )
        self.wait(0.4)
