from manim import *
import numpy as np
import os

config.media_dir = "/Users/williamchang/Downloads"
# Optional: put the MP4s directly in Downloads
config.custom_folders = True
config.video_dir = "/Users/williamchang/Downloads"


class BanditShow(Scene):
    """
    Toggle segments by setting the booleans in SEGMENTS (or via env vars).
    Order in `construct()` defines the final stitching.
    """

    # --- Global knobs (you can also set these via env vars) ---
    SEED_PULLS = int(os.getenv("SEED_PULLS", "7"))
    SEED_MEAN  = int(os.getenv("SEED_MEAN", "42"))

    # Segment toggles (override with env vars like: SEG_BANDIT=0)
    SEGMENTS = {
        "bandit_intro": bool(int(os.getenv("SEG_BANDIT", "1"))),
        "empirical_mean": bool(int(os.getenv("SEG_EMPMEAN", "0"))),
        "subgaussian": bool(int(os.getenv("SEG_SUBG", "0"))),
        "regret_decomp": bool(int(os.getenv("SEG_REGRET", "0"))),
    }

    # Shared parameters
    mus    = [0.6, 0.2, 0.8, 0.4]
    sigmas = [0.15, 0.1, 0.2, 0.12]
    n_pulls = 5

    def construct(self):
        # Stitch the segments in the order you want
        if self.SEGMENTS["bandit_intro"]:
            self.segment_bandit_intro()

        if self.SEGMENTS["empirical_mean"]:
            self.segment_empirical_mean()

        if self.SEGMENTS["subgaussian"]:
            self.segment_subgaussian()

        if self.SEGMENTS["regret_decomp"]:
            self.segment_regret_decomposition()

        # -----------------------------
    # Segment 1: Bandit intro + random pulls
    # -----------------------------
    def segment_bandit_intro(self):
        np.random.seed(self.SEED_PULLS)

        header = Text("Bandit Arms and Reward Means", font_size=36).to_edge(UP)
        self.play(FadeIn(header))

        # Layout + elements
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

            # Smaller inside labels
            a_label = MathTex(fr"a_{i+1}").scale(0.7).move_to(circle.get_center())
            action_labels.add(a_label)

            # Alternate above/below placement for distribution labels
            direction = UP if (i % 2 == 0) else DOWN
            dist_tex = MathTex(
                r"\mathcal{N}\!\left(" + f"{mu:.2f}" + r",\, " + f"{sigma:.2f}" + r"\right)"
            ).scale(0.8).next_to(circle, direction, buff=dist_label_y_offset)
            dist_labels.add(dist_tex)

        self.play(FadeIn(action_circles), Write(action_labels))
        self.play(Write(dist_labels))
        self.wait(0.4)

        # Legend
        legend = VGroup(
            Dot().set_fill(YELLOW, opacity=0.9), Text("pull highlight", font_size=22),
            Dot().set_fill(GREEN, opacity=0.35),  Text("visited", font_size=22),
        ).arrange(RIGHT, buff=0.3).to_edge(DOWN)
        self.play(FadeIn(legend))

        # -----------------------------
        # Random pulls (also log for table)
        # -----------------------------
        pulls = np.random.randint(0, len(self.mus), size=self.n_pulls)

        # Keep a log for the table: [round, arm, reward, mean]
        table_rows = []
        sum_rewards = 0.0
        sum_means   = 0.0

        for t, arm_idx in enumerate(pulls, start=1):
            circle = action_circles[arm_idx]
            center = circle.get_center()

            # Highlight
            self.play(
                circle.animate.set_fill(YELLOW, opacity=0.9).set_stroke(YELLOW_E, width=3),
                run_time=0.3
            )

            # Reward pop
            reward = np.random.normal(self.mus[arm_idx], self.sigmas[arm_idx])
            reward_text = DecimalNumber(reward, num_decimal_places=3).scale(0.7)
            reward_text.move_to(center + UP * 1.0)

            bubble = RoundedRectangle(corner_radius=0.1, width=2.1, height=0.6)\
                .set_fill(WHITE, opacity=0.15).set_stroke(WHITE, opacity=0.4, width=1)\
                .move_to(reward_text.get_center())

            pull_label = Text(f"Pull {t}: a_{arm_idx+1}", font_size=26).next_to(header, DOWN)

            self.play(FadeIn(bubble, scale=0.9), FadeIn(reward_text, shift=UP*0.2),
                    FadeTransformPieces(header.copy(), pull_label), run_time=0.4)
            self.wait(0.2)

            self.play(reward_text.animate.shift(UP * 0.5),
                    bubble.animate.shift(UP * 0.5).set_opacity(0.05),
                    rate_func=smooth, run_time=0.35)
            self.play(FadeOut(reward_text), FadeOut(bubble), FadeOut(pull_label), run_time=0.25)

            # Mark visited
            self.play(
                circle.animate.set_fill(GREEN, opacity=0.35).set_stroke(GREEN_E, width=2),
                run_time=0.2
            )
            self.wait(0.05)

            # Log the row for the table
            mean_val = self.mus[arm_idx]
            table_rows.append([
                f"{t}",
                f"a_{arm_idx+1}",
                f"{reward:.3f}",
                f"{mean_val:.3f}",
            ])
            sum_rewards += reward
            sum_means   += mean_val

        # Fade out setup before showing the table
        self.play(
            FadeOut(legend),
            FadeOut(dist_labels),
            FadeOut(action_labels),
            FadeOut(action_circles),
            FadeOut(header),
            run_time=0.6
        )
        self.wait(0.4)

        # -----------------------------
        # New Section: Results Table
        # -----------------------------
        self.wait(0.6)

        # (A) Sanitize rows (prevents a stray blank row)
        table_rows = [row for row in table_rows if len(row) == 4 and all(str(x).strip() for x in row)]
        n_rows = len(table_rows)

        # (B) Column headers + descriptions
        col_labels = [
            Text("Round #", font_size=26),
            Text("Arm Pulled", font_size=26),
            Text("Reward", font_size=26),
            Text("Mean", font_size=26),
        ]

        results_table = Table(
            table_rows,                  # data ONLY (no header row inside table_rows)
            col_labels=col_labels,
            include_outer_lines=True,
            h_buff=0.6,
            v_buff=0.3,
        ).scale(0.7)

        # Position the table slightly lower
        results_table.to_edge(UP, buff=2.0)   # <- higher buff = lower position
        results_table.shift(DOWN * 0.2)       # <- nudge a bit more if you like

        # Build pieces & hide body entries (so we can reveal them ourselves)
        grid_h = results_table.get_horizontal_lines()
        grid_v = results_table.get_vertical_lines()
        headers = results_table.get_col_labels()
        body_entries = results_table.get_entries_without_labels()   # VGroup of all body cells (text)

        for m in body_entries:
            m.set_opacity(0)

        # Column descriptions (hover text above headers; not an extra row)
        col_descs = VGroup(
            Text("time index", font_size=18).next_to(headers[0], UP, buff=0.25),
            Text("which arm", font_size=18).next_to(headers[1], UP, buff=0.25),
            Text("sampled value", font_size=18).next_to(headers[2], UP, buff=0.20),
            Text("arm mean", font_size=18).next_to(headers[3], UP, buff=0.25),
        )

        # Draw grid + headers + descriptions (removed FadeIn(col_descs))
        self.play(Create(grid_h), Create(grid_v), FadeIn(headers), run_time=0.6)

        # -----------------------------
        # Row-by-row reveal with counting numbers
        # -----------------------------
        for r in range(1, n_rows + 1):
            # Cells (rectangles) to position content
            c_round  = results_table.get_cell((r + 1, 1))
            c_arm    = results_table.get_cell((r + 1, 2))
            c_reward = results_table.get_cell((r + 1, 3))
            c_mean   = results_table.get_cell((r + 1, 4))

            # Values
            round_val  = int(table_rows[r-1][0])
            arm_str    = table_rows[r-1][1]    # <- Arm Pulled text
            reward_val = float(table_rows[r-1][2])
            mean_val   = float(table_rows[r-1][3])

            # Arm Pulled – explicit label to guarantee it appears
            arm_label = MathTex(arm_str, font_size=24).move_to(c_arm.get_center())
            self.play(FadeIn(arm_label, scale=0.9, shift=0.1*UP), run_time=0.2)

            # Animated counters for Round/Reward/Mean
            vt_round  = ValueTracker(0)
            dn_round  = always_redraw(lambda:
                Integer(int(vt_round.get_value())).scale(0.6).move_to(c_round.get_center())
            )
            vt_reward = ValueTracker(0.0)
            dn_reward = always_redraw(lambda:
                DecimalNumber(vt_reward.get_value(), num_decimal_places=3).scale(0.6).move_to(c_reward.get_center())
            )
            vt_mean   = ValueTracker(0.0)
            dn_mean   = always_redraw(lambda:
                DecimalNumber(vt_mean.get_value(), num_decimal_places=3).scale(0.6).move_to(c_mean.get_center())
            )

            # Add counters to scene
            self.add(dn_round, dn_reward, dn_mean)

            # Optional row highlight
            row_group = VGroup(c_round, c_arm, c_reward, c_mean)
            highlight = SurroundingRectangle(row_group, color=YELLOW, buff=0.08, stroke_width=2)
            self.play(Create(highlight), run_time=0.18)

            # Make sure the Arm Pulled (col 2) shows up:
            # Option 1: fade in the table's own entry
            # arm_entry = results_table.get_entries((r, 2))
            # self.play(FadeIn(arm_entry, scale=0.9, shift=0.1*UP), run_time=0.2)

            # (If you ever prefer your own label instead of the table's entry, use:)
            # arm_label = Text(arm_str, font_size=26).move_to(c_arm.get_center())
            # self.play(FadeIn(arm_label, scale=0.9, shift=0.1*UP), run_time=0.2)

            # Count up numbers
            self.play(
                vt_round.animate.set_value(round_val),
                vt_reward.animate.set_value(reward_val),
                vt_mean.animate.set_value(mean_val),
                run_time=0.6,
                rate_func=smooth,
            )

            self.play(FadeOut(highlight), run_time=0.12)

            # Bake counters (remove updaters)
            dn_round.clear_updaters();  dn_round.set_value(round_val)
            dn_reward.clear_updaters(); dn_reward.set_value(reward_val)
            dn_mean.clear_updaters();   dn_mean.set_value(mean_val)

        self.wait(0.4)

        # Totals below the (now lower) table
        totals = VGroup(
            Text(f"Sum of rewards: {sum_rewards:.3f}", font_size=28),
            Text(f"Sum of means:   {sum_means:.3f}", font_size=28),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.15).next_to(results_table, DOWN, buff=0.5)

        self.play(GrowFromCenter(totals), run_time=0.4)
        self.wait(0.8)


    # -----------------------------
    # Segment 2: Empirical mean animation
    # -----------------------------
    def segment_empirical_mean(self):
        header = Text("Empirical Mean Calculation from Samples", font_size=34).to_edge(UP)
        self.play(FadeIn(header))

        mu, sigma, n_samples = 0.5, 1.0, 10
        np.random.seed(self.SEED_MEAN)
        samples = np.random.normal(mu, sigma, n_samples)
        means = np.cumsum(samples) / np.arange(1, n_samples + 1)

        axes = Axes(
            x_range=[-1, 2, 0.5], y_range=[0, 0.5, 0.1],
            x_length=6, y_length=1.2
        ).shift(UP * 1.6)
        bell_curve = axes.plot(
            lambda x: (1 / np.sqrt(2 * np.pi * sigma ** 2)) * np.exp(-0.5 * ((x - mu) / sigma) ** 2),
            color=PURPLE
        )
        dist_formula = MathTex(r"X_t \sim \mathcal{N}(0.5,\ 1^2)").next_to(axes, UP)

        self.play(Create(axes), Create(bell_curve), Write(dist_formula))
        self.wait(0.3)

        number_line = NumberLine(x_range=[-1, 2, 0.5], length=7, include_numbers=True).to_edge(DOWN)
        self.play(Create(number_line))
        mu_dot = Dot(number_line.n2p(mu), color=YELLOW)
        mu_label = MathTex(r"\mu").next_to(mu_dot, UP)
        self.play(FadeIn(mu_dot), Write(mu_label))

        for i in range(n_samples):
            x_val = samples[i]
            bell_y = (1 / np.sqrt(2 * np.pi * sigma ** 2)) * np.exp(-0.5 * ((x_val - mu) / sigma) ** 2)
            dot_bell = Dot(axes.c2p(x_val, bell_y), color=BLUE)
            self.play(GrowFromCenter(dot_bell), run_time=0.25)

            sample_text = MathTex(f"{x_val:.2f}").scale(0.6).next_to(dot_bell, UP, buff=0.07)
            self.play(FadeIn(sample_text), run_time=0.15)

            terms = "+".join([f"{samples[j]:.2f}" for j in range(i + 1)])
            formula_tex = MathTex(r"\hat\mu = \frac{" + terms + r"}{" + f"{i+1}" + r"}")\
                .to_edge(LEFT).shift(DOWN * 0.6)
            self.play(Write(formula_tex)); self.wait(0.25)
            self.play(FadeOut(formula_tex), FadeOut(dot_bell), FadeOut(sample_text))

            emp_mean = means[i]
            mean_dot = Dot(number_line.n2p(emp_mean), color=RED)
            mean_label = MathTex(r"\hat\mu").next_to(mean_dot, UP)
            n_label = Text(f"n={i+1}", font_size=28).next_to(mean_dot, DOWN)
            self.play(FadeIn(mean_dot), FadeIn(mean_label), FadeIn(n_label), run_time=0.35)
            self.wait(0.4)
            self.play(FadeOut(mean_dot), FadeOut(mean_label), FadeOut(n_label), run_time=0.2)

        self.play(FadeOut(number_line), FadeOut(mu_dot), FadeOut(mu_label),
                  FadeOut(axes), FadeOut(bell_curve), FadeOut(dist_formula), FadeOut(header))

    # -----------------------------
    # Segment 3: Sub-Gaussian bound plots
    # -----------------------------
    def segment_subgaussian(self):
        header = Text("Sub-Gaussian Concentration Bound", font_size=36).to_edge(UP)
        self.play(FadeIn(header))

        formula = MathTex(
            r"\mathbb{P}\left(\hat\mu \geq \mu+\varepsilon\right) \leq \exp\!\left(-\frac{n\varepsilon^2}{2\sigma^2}\right)"
        ).to_edge(UP, buff=1.5)
        self.play(Write(formula)); self.wait(0.7)

        # Fix sigma for both plots
        sigma = 1.0

        # P vs n (eps fixed)
        axes1 = Axes(
            x_range=[0, 40, 5], y_range=[0, 1, 0.1],
            x_length=6, y_length=3.2, axis_config={"include_tip": False}
        ).shift(LEFT*3 + DOWN*0.5)
        eps = 0.5
        graph1 = axes1.plot(lambda n: np.exp(-n * eps**2 / (2 * sigma**2)), x_range=[0, 40], color=BLUE)
        label1 = MathTex(r"\varepsilon=0.5,\ \sigma=1").next_to(axes1, UP)
        axes1_labels = axes1.get_axis_labels(MathTex("n"))
        self.play(Create(axes1), Write(axes1_labels), FadeIn(label1))
        self.play(Create(graph1), run_time=1.8)
        self.wait(0.6)
        self.play(FadeOut(VGroup(axes1, axes1_labels, label1, graph1)))

        # P vs eps (n fixed)
        axes2 = Axes(
            x_range=[0, 2, 0.2], y_range=[0, 1, 0.1],
            x_length=6, y_length=3.2, axis_config={"include_tip": False}
        ).shift(RIGHT*3 + DOWN*0.5)
        n_fixed = 20
        graph2 = axes2.plot(lambda e: np.exp(-n_fixed * e**2 / (2 * sigma**2)),
                            x_range=[0, 2], color=GREEN)
        label2 = MathTex(r"n=20,\ \sigma=1").next_to(axes2, UP)
        axes2_labels = axes2.get_axis_labels(MathTex(r"\varepsilon"))
        self.play(Create(axes2), Write(axes2_labels), FadeIn(label2))
        self.play(Create(graph2), run_time=1.8)
        self.wait(0.8)

        self.play(FadeOut(VGroup(axes2, axes2_labels, label2, graph2, formula, header)))

    # -----------------------------
    # Segment 4: Regret decomposition table
    # -----------------------------
    def segment_regret_decomposition(self):
        header = Text("Regret and Suboptimality Gap", font_size=36).to_edge(UP)
        self.play(FadeIn(header))

        regret = MathTex(r"R_T = \sum_{t=1}^T \left(\mu^* - \mathbb{E}[X_{a_{n_t}}]\right)").scale(1.05)
        self.play(Write(regret)); self.wait(1.0)
        self.play(FadeOut(regret))

        subopt_gap = MathTex(r"\Delta_a = \mu^* - \mu_a").scale(1.2)
        self.play(Write(subopt_gap)); self.wait(0.9)
        self.play(FadeOut(subopt_gap), FadeOut(header))

        # Table section
        ARM_MEANS = [0.5, 0.8, 0.3]
        ARM_COLORS = [BLUE, GREEN, RED]
        PULL_SEQUENCE = [0, 1, 2, 1, 0, 1]

        np.random.seed(self.SEED_MEAN)
        REWARDS = [np.random.normal(ARM_MEANS[a], 0.1) for a in PULL_SEQUENCE]
        MU_STAR = max(ARM_MEANS)
        DELTAS = [MU_STAR - ARM_MEANS[a] for a in PULL_SEQUENCE]

        headers = [r"\text{Round } $t$", r"$\mu_a$", r"\text{Reward}", r"$\Delta_a$"]
        rounds = list(range(1, len(PULL_SEQUENCE)+1))
        means = [f"{ARM_MEANS[a]:.2f}" for a in PULL_SEQUENCE]
        rewards = [f"{r:.2f}" for r in REWARDS]
        deltas_init = [""]*len(PULL_SEQUENCE)

        table_data = [[str(t), mu, r, d] for t, mu, r, d in zip(rounds, means, rewards, deltas_init)]
        table = Table(
            table_data,
            col_labels=[Tex(h) for h in headers],
            include_outer_lines=True,
            top_left_entry=None,
        ).scale(0.9).to_edge(UP)

        self.add(table)

        # Highlight reward col
        reward_highlight = SurroundingRectangle(table.get_columns()[2], color=YELLOW, buff=0.1)
        self.play(Create(reward_highlight)); self.wait(1.0)
        self.play(FadeOut(reward_highlight))

        # Highlight mean col
        mean_highlight = SurroundingRectangle(table.get_columns()[1], color=ORANGE, buff=0.1)
        self.play(Create(mean_highlight)); self.wait(0.6)

        # Fill delta column
        delta_col = table.get_columns()[3]
        for i, cell in enumerate(delta_col):
            if i < len(PULL_SEQUENCE):
                arm = PULL_SEQUENCE[i]
                delta_tex = MathTex(f"{DELTAS[i]:.2f}").set_color(ARM_COLORS[arm])
                self.play(Transform(cell, delta_tex), run_time=0.35)

        self.wait(0.6)
        self.play(FadeOut(mean_highlight))

        regret_text = MathTex(r"\text{Per-round regret} = \Delta_a = \mu^* - \mu_a")\
            .next_to(table, DOWN, buff=1).scale(0.9)
        self.play(Write(regret_text)); self.wait(0.9)

        # Group per-arm contributions
        group_labels = ["a_1", "a_2", "a_3"]
        groups = [[] for _ in range(3)]
        for i, arm in enumerate(PULL_SEQUENCE):
            groups[arm].append(i)

        for arm, indices in enumerate(groups):
            if not indices:
                continue
            cell_group = VGroup(*[table.get_columns()[3][i] for i in indices])
            rect = SurroundingRectangle(cell_group, color=ARM_COLORS[arm], buff=0.1)
            self.play(Create(rect), run_time=0.4)

            group_sum = MathTex(
                r"\sum",
                MathTex(group_labels[arm]).set_color(ARM_COLORS[arm]),
                r":\quad" + "+".join([f"{DELTAS[i]:.2f}" for i in indices]) +
                f" = {sum([DELTAS[i] for i in indices]):.2f}"
            ).set_color(ARM_COLORS[arm]).scale(0.75)
            group_sum.next_to(rect, RIGHT, buff=0.15)
            self.play(Write(group_sum), run_time=0.4)

        total_regret = sum(DELTAS)
        total_text = MathTex(
            r"\text{Total regret} = ", "+".join([f"{d:.2f}" for d in DELTAS]), f"= {total_regret:.2f}"
        ).set_color(PURPLE).next_to(regret_text, DOWN, buff=0.8).scale(1.0)
        self.play(Write(total_text)); self.wait(1.2)

        self.play(
            *[FadeOut(mob) for mob in self.mobjects if mob is not total_text],
            total_text.animate.move_to(ORIGIN)
        )
        self.wait(0.8)
