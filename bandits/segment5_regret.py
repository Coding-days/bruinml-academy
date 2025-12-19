from manim import *
import numpy as np

# Optional: put outputs in Downloads (same as before)
config.media_dir = "/Users/williamchang/Downloads"
config.custom_folders = True
config.video_dir = "/Users/williamchang/Downloads"


class RegretDecomposition(Scene):
    def construct(self):
        self.segment_regret_decomposition()

    # -------------------------------------------------
    # Regret decomposition table + derivation
    # -------------------------------------------------
    def segment_regret_decomposition(self):
        header = Text("Regret and Suboptimality Gap", font_size=36).to_edge(UP)
        self.play(FadeIn(header))

        # --- Setup ---
        ARM_MEANS = [0.5, 0.8, 0.3]
        ARM_COLORS = [BLUE, GREEN, RED]
        PULL_SEQUENCE = [0, 1, 2, 1, 0, 1]

        np.random.seed(42)
        REWARDS = [np.random.normal(ARM_MEANS[a], 0.1) for a in PULL_SEQUENCE]

        MU_STAR = max(ARM_MEANS)
        DELTA_BY_ARM = [MU_STAR - m for m in ARM_MEANS]
        DELTAS = [DELTA_BY_ARM[a] for a in PULL_SEQUENCE]
        PER_ROUND_REGRET = DELTAS

        # --- Arm Visualization Setup ---
        x_spacing = 1.7
        radius = 0.4
        mean_label_y_offset = 0.6

        action_circles = VGroup()
        action_labels = VGroup()
        mean_labels = VGroup()

        for i, mu in enumerate(ARM_MEANS):
            x_shift = RIGHT * x_spacing * (i - (len(ARM_MEANS) - 1) / 2)

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
            mu_tex = MathTex(rf"\mu_{i+1} = {mu:.2f}").scale(0.8).next_to(
                circle, direction, buff=mean_label_y_offset
            )
            mean_labels.add(mu_tex)

        self.play(FadeIn(action_circles), Write(action_labels))
        self.play(Write(mean_labels))
        self.wait(0.4)

        legend = VGroup(
            Dot().set_fill(YELLOW, opacity=0.9), Text("pull highlight", font_size=22),
            Dot().set_fill(GREEN, opacity=0.35), Text("visited", font_size=22),
        ).arrange(RIGHT, buff=0.3).to_edge(DOWN)
        self.play(FadeIn(legend))

        # --- Animate Pulls ---
        for t, arm_idx in enumerate(PULL_SEQUENCE, start=1):
            circle = action_circles[arm_idx]
            center = circle.get_center()

            self.play(
                circle.animate.set_fill(YELLOW, opacity=0.9).set_stroke(YELLOW_E, width=3),
                run_time=0.3
            )

            reward = REWARDS[t-1]
            reward_text = Text(f"{reward:.3f}", font_size=28).move_to(center + UP * 1.0)

            bubble = (
                RoundedRectangle(corner_radius=0.1, width=2.1, height=0.6)
                .set_fill(WHITE, opacity=0.15)
                .set_stroke(WHITE, opacity=0.4, width=1)
                .move_to(reward_text.get_center())
            )

            pull_label = MathTex(rf"\text{{Pull {t}: }} a_{{{arm_idx+1}}}", font_size=26).next_to(header, DOWN)

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

        # --- Cleanup Arms ---
        self.play(
            FadeOut(legend),
            FadeOut(mean_labels),
            FadeOut(action_labels),
            FadeOut(action_circles),
            FadeOut(header),
            run_time=0.6
        )
        self.wait(0.4)

        # --- Definitions ---
        regret_def = MathTex(r"R_T = \sum_{t=1}^T r_t", font_size=40)\
            .next_to(header, DOWN, buff=0.35)
        gap_def = MathTex(r"\Delta_a = \mu^{\star} - \mu_a", font_size=40)\
            .next_to(regret_def, DOWN, buff=0.25)

        self.play(Write(regret_def))
        self.play(Write(gap_def))
        self.wait(0.6)
        self.play(FadeOut(VGroup(regret_def, gap_def, header)))

        # =====================================================
        # Frame 1: Table with regret + gap columns
        # =====================================================
        header2 = Text("Per-Round Regret and Gaps", font_size=34).to_edge(UP)
        self.play(FadeIn(header2))

        headers = [
            r"\text{Round } t",
            r"a_t",
            r"\mu_{a_t}",
            r"X_t",
            r"r_t",
            r"\Delta_{a_t}",
        ]

        table_data = []
        for t, a in enumerate(PULL_SEQUENCE, start=1):
            table_data.append([
                str(t),
                rf"a_{{{a+1}}}",
                f"{ARM_MEANS[a]:.2f}",
                f"{REWARDS[t-1]:.2f}",
                "",
                "",
            ])

        table = Table(
            table_data,
            col_labels=[MathTex(h) for h in headers],
            include_outer_lines=True,
            h_buff=0.55,
            v_buff=0.28,
        ).scale(0.78).to_edge(UP, buff=1.2)

        self.add(table)

        rt_col = table.get_columns()[4]
        delta_col = table.get_columns()[5]

        for i, arm in enumerate(PULL_SEQUENCE):
            rt_tex = MathTex(f"{PER_ROUND_REGRET[i]:.2f}")\
                .set_color(ARM_COLORS[arm])
            delta_tex = MathTex(f"{DELTAS[i]:.2f}")\
                .set_color(ARM_COLORS[arm])

            self.play(
                Transform(rt_col[i + 1], rt_tex),
                Transform(delta_col[i + 1], delta_tex),
                run_time=0.5
            )

        note = MathTex(r"r_t = \Delta_{a_t}", font_size=34)\
            .next_to(table, DOWN, buff=0.45)
        self.play(Write(note))
        self.wait(0.8)

        # =====================================================
        # Frame 2: Total regret = sum of gaps
        # =====================================================
        self.play(FadeOut(VGroup(table, note, header2)))

        header3 = Text("Total Regret", font_size=36).to_edge(UP)
        self.play(FadeIn(header3))

        delta_terms = [f"{d:.2f}" for d in DELTAS]
        total_regret = sum(DELTAS)

        line1 = MathTex(r"R_T = \sum_{t=1}^T \Delta_{a_t}", font_size=42)\
            .next_to(header3, DOWN, buff=0.4)
        line2 = MathTex(
            r"= " + " + ".join(delta_terms) + rf" = {total_regret:.2f}",
            font_size=40
        ).next_to(line1, DOWN, buff=0.3)

        self.play(Write(line1))
        self.play(Write(line2))
        self.wait(0.8)

        # =====================================================
        # Frame 3: Regroup by arms → decomposition
        # =====================================================
        self.play(FadeOut(VGroup(line1, line2)))

        header4 = Text("Regret Decomposition", font_size=36).to_edge(UP)
        self.play(Transform(header3, header4))

        groups = {0: [], 1: [], 2: []}
        for i, a in enumerate(PULL_SEQUENCE):
            groups[a].append(i)

        blocks = VGroup()
        for a in [0, 1, 2]:
            terms = [f"{DELTAS[i]:.2f}" for i in groups[a]]
            block = MathTex(
                rf"\underbrace{{" + " + ".join(terms) +
                rf"}}_{{\text{{pulls of }}a_{{{a+1}}}}}",
                font_size=38
            ).set_color(ARM_COLORS[a])
            blocks.add(block)

        blocks.arrange(DOWN, aligned_edge=LEFT, buff=0.35)\
              .next_to(header4, DOWN, buff=0.6)

        self.play(FadeIn(blocks))
        self.wait(0.6)

        final_identity = MathTex(
            r"R_T = \sum_{a=1}^K N_a(T)\,\Delta_a",
            font_size=46
        ).next_to(blocks, DOWN, buff=0.6)

        box = SurroundingRectangle(final_identity, buff=0.18)
        self.play(Write(final_identity), Create(box))
        self.wait(1.2)

        self.play(FadeOut(VGroup(header4, blocks, final_identity, box)))
