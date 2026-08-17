from manim import *
import random

random.seed(42)

class MultiArmedBandit(Scene):
    def construct(self):
        # ── Helpers ──
        def cap(text, **kwargs):
            return Text(text, font_size=26, **kwargs).to_edge(DOWN, buff=0.45)

        def clear(*mobjects):
            self.play(*[FadeOut(m) for m in mobjects])

        def section_title(text):
            t = Text(text, font_size=40, weight=BOLD, color=YELLOW)
            self.play(FadeIn(t))
            self.wait(1.5)
            self.play(FadeOut(t))

        # ============================
        # 1. TITLE
        # ============================
        title = Text("Standard Multi-Armed\nBandit", font_size=52, weight=BOLD)
        subtitle = Text(
            "A Stochastic Framework",
            font_size=28, color=GREY
        ).next_to(title, DOWN, buff=0.4)
        self.play(Write(title), run_time=1.5)
        self.play(FadeIn(subtitle, shift=UP * 0.2))
        self.wait(2)
        clear(title, subtitle)

        # ============================
        # 2. THE ARMS
        # ============================
        section_title("The Setup")

        c1 = cap("We have K actions,\ncalled arms.")
        arms_eq = MathTex(
            r"\mathcal{A} = \{a_1, a_2, \dots, a_K\}",
            font_size=44
        )
        self.play(Write(arms_eq), FadeIn(c1))
        self.wait(2.5)
        clear(arms_eq, c1)

        # ============================
        # 3. SLOT MACHINES + ARM PULL DEMO
        # ============================
        # -- Build 3 slot machines with true means shown --
        arm_colors = [RED, BLUE, GREEN]
        arm_names = ["a_1", "a_2", "a_3"]
        true_means = [0.8, 0.5, 0.7]

        machines = VGroup()
        for i in range(3):
            body = RoundedRectangle(
                width=1.6, height=2.4, corner_radius=0.2,
                fill_color=arm_colors[i], fill_opacity=0.25,
                stroke_color=arm_colors[i], stroke_width=2.5
            )
            name = MathTex(arm_names[i], font_size=32).move_to(body).shift(UP * 0.4)
            # Show true mean inside machine (dimmed)
            mu_label = MathTex(
                r"\mu_{" + str(i+1) + r"} = " + str(true_means[i]),
                font_size=22, color=GREY_B
            ).move_to(body).shift(DOWN * 0.5)
            machines.add(VGroup(body, name, mu_label))

        machines.arrange(RIGHT, buff=0.8).shift(UP * 0.8)

        c2 = cap("Each arm is like\na slot machine.")
        self.play(
            LaggedStart(*[FadeIn(m, shift=UP*0.3) for m in machines], lag_ratio=0.2),
            FadeIn(c2)
        )
        self.wait(2)
        self.play(FadeOut(c2))

        # -- Now demonstrate pulling arms --
        c3 = cap("At each round, we pull\nan arm and get a reward.")
        self.play(FadeIn(c3))
        self.wait(1.5)
        self.play(FadeOut(c3))

        c4 = cap("The reward is random.\nIt need not equal\nthe true mean.")
        self.play(FadeIn(c4))
        self.wait(0.5)

        # Pull sequence: arm indices 0,1,2,0,2
        pull_sequence = [0, 1, 2, 0, 2]
        # Pre-generate stochastic rewards near the true means
        stochastic_rewards = [0.72, 0.61, 0.65, 0.88, 0.74]

        reward_texts_all = VGroup()  # to clean up later

        for pull_idx, (arm_i, reward_val) in enumerate(zip(pull_sequence, stochastic_rewards)):
            machine = machines[arm_i]
            body = machine[0]

            # Highlight: glow effect via surrounding rect
            highlight = body.copy().set_stroke(YELLOW, width=6).set_fill(opacity=0)
            self.play(Create(highlight), run_time=0.3)

            # Reward pops out above the machine
            reward_text = MathTex(
                str(reward_val),
                font_size=30, color=YELLOW
            ).next_to(machine, UP, buff=0.25)
            mean_compare = MathTex(
                r"\mu_{" + str(arm_i+1) + r"} = " + str(true_means[arm_i]),
                font_size=22, color=GREY_A
            ).next_to(reward_text, UP, buff=0.15)

            self.play(
                FadeIn(reward_text, shift=UP * 0.3),
                FadeIn(mean_compare, shift=UP * 0.2),
                run_time=0.5
            )
            self.wait(1.0)

            # Fade reward and highlight before next pull
            self.play(
                FadeOut(highlight),
                FadeOut(reward_text),
                FadeOut(mean_compare),
                run_time=0.4
            )

        self.play(FadeOut(c4))

        c5 = cap("Notice: rewards fluctuate\naround the true mean,\nbut never reveal it exactly.")
        self.play(FadeIn(c5))
        self.wait(2.5)
        clear(machines, c5)

        # ============================
        # 4. FORMAL REWARD NOTATION
        # ============================
        c6 = cap("Formally, at round t\nwe pick arm A_t and\nreceive reward X.")
        round_eq = MathTex(
            r"\text{Round } t:",
            r"\;\; A_t \in \mathcal{A}",
            r"\;\Rightarrow\;",
            r"X_{a_{n_t}} \in [0,1]",
            font_size=38
        )
        self.play(Write(round_eq), FadeIn(c6))
        self.wait(3)
        clear(round_eq, c6)

        # ============================
        # 5. MEAN REWARDS
        # ============================
        c7 = cap("Each arm has a fixed\nbut unknown mean reward.")
        mu_eq = MathTex(
            r"\mu_i = \mathbb{E}[X_{a_i}(t)]",
            font_size=44
        )
        self.play(Write(mu_eq), FadeIn(c7))
        self.wait(2.5)
        clear(mu_eq, c7)

        # ============================
        # 6. OPTIMAL ARM
        # ============================
        c8 = cap("The best arm's mean\nis called mu-star.")
        mustar_eq = MathTex(
            r"\mu^\star = \max_{a_i \in \mathcal{A}} \mu_i",
            font_size=44
        )
        self.play(Write(mustar_eq), FadeIn(c8))
        self.wait(2.5)
        clear(mustar_eq, c8)

        # ============================
        # 7. GOAL
        # ============================
        c9 = cap("Our goal: maximize\ntotal expected rewards.")
        goal_eq = MathTex(
            r"\text{Maximize } \; \mathbb{E}\!\left[\sum_{t=1}^T X_{a_{n_t}}\right]",
            font_size=40
        )
        self.play(Write(goal_eq), FadeIn(c9))
        self.wait(2.5)
        clear(goal_eq, c9)

        # ============================
        # 8. REGRET DEFINITION
        # ============================
        section_title("Regret")

        c10 = cap("Regret measures loss\ncompared to the best arm.")
        regret_eq = MathTex(
            r"R_T", r"=", r"T\mu^\star", r"-",
            r"\mathbb{E}\!\left[\sum_{t=1}^T X_{a_{n_t}}\right]",
            font_size=38
        ).shift(UP * 0.5)
        self.play(Write(regret_eq), FadeIn(c10))
        self.wait(3)

        self.play(FadeOut(c10))
        c10b = cap("Equivalently, it sums\nexpected losses each round.")
        regret_eq2 = MathTex(
            r"= \sum_{t=1}^T",
            r"\mathbb{E}\!\left[\mu^\star - \mu_{a_{n_t}}\right]",
            font_size=38
        ).next_to(regret_eq, DOWN, buff=0.35, aligned_edge=LEFT).shift(RIGHT * 0.3)
        self.play(Write(regret_eq2), FadeIn(c10b))
        self.wait(3)
        clear(regret_eq, regret_eq2, c10b)

        # ============================
        # 9. REGRET DECOMPOSITION
        # ============================
        c11 = cap("We can also decompose\nregret by arm.")
        decomp_eq = MathTex(
            r"R_T = \sum_{a_i \in \mathcal{A}} \Delta_i \, \mathbb{E}[n_i(T\!+\!1)]",
            font_size=40
        ).shift(UP * 0.5)
        n_explain = Text(
            "n_i(T) = number of times\narm i is pulled",
            font_size=24, color=GREY_B
        ).next_to(decomp_eq, DOWN, buff=0.5)
        self.play(Write(decomp_eq), FadeIn(c11))
        self.wait(1.5)
        self.play(FadeIn(n_explain, shift=UP * 0.2))
        self.wait(2.5)
        clear(decomp_eq, n_explain, c11)

        # ============================
        # 10. COIN FLIP ANALOGY (EXPANDED)
        # ============================
        section_title("Why Can't We See Regret?")

        # --- Part A: Setup the coin ---
        c12 = cap("Imagine a coin with\nan unknown probability\nof landing heads.")
        coin = Circle(
            radius=0.7, fill_color=GOLD, fill_opacity=0.6,
            stroke_color=GOLD_E, stroke_width=3
        ).shift(UP * 1.5)
        q_mark = Text("?", font_size=44, weight=BOLD, color=BLACK).move_to(coin)
        coin_grp = VGroup(coin, q_mark)

        true_p_label = MathTex(
            r"\text{True } p = \;???",
            font_size=30, color=GREY_A
        ).next_to(coin_grp, RIGHT, buff=0.6)

        self.play(FadeIn(coin_grp, scale=0.5), FadeIn(c12))
        self.wait(1)
        self.play(FadeIn(true_p_label))
        self.wait(2)
        self.play(FadeOut(c12))

        # --- Part B: Simulate flips with running estimate ---
        c13 = cap("Let's flip it and\ntrack our estimate.")
        self.play(FadeIn(c13))

        # We'll show a few rounds of flipping
        # True p = 0.6 (unknown to us)
        true_p = 0.6
        random.seed(7)
        flip_results = [random.random() < true_p for _ in range(12)]

        heads_count = 0
        total_count = 0

        # Display area for flip results and running estimate
        flip_display = Text("Flips: ", font_size=22).shift(DOWN * 0.0).to_edge(LEFT, buff=0.8)
        estimate_display = MathTex(
            r"\hat{p} = ?",
            font_size=30
        ).shift(DOWN * 1.0)
        self.play(FadeIn(flip_display), FadeIn(estimate_display))

        flip_symbols = VGroup()

        for i, is_heads in enumerate(flip_results):
            total_count += 1
            if is_heads:
                heads_count += 1
                sym = Text("H", font_size=20, color=GREEN_B)
            else:
                sym = Text("T", font_size=20, color=RED_B)

            sym.next_to(flip_display, RIGHT, buff=0.1 + i * 0.35)
            if i >= 8:
                sym.next_to(flip_display, RIGHT, buff=0.1 + (i - 8) * 0.35).shift(DOWN * 0.35)
            flip_symbols.add(sym)

            est_val = heads_count / total_count
            new_estimate = MathTex(
                r"\hat{p} = " + f"{heads_count}/{total_count} = {est_val:.2f}",
                font_size=30
            ).move_to(estimate_display)

            self.play(
                FadeIn(sym, shift=DOWN * 0.15),
                Transform(estimate_display, new_estimate),
                run_time=0.35
            )

        self.wait(1.5)
        self.play(FadeOut(c13))

        # --- Part C: Reveal the point ---
        c14 = cap("After 12 flips, our\nestimate is close but\nnot the true value.")
        self.play(FadeIn(c14))
        self.wait(2)

        # Now reveal the true p
        true_reveal = MathTex(
            r"\text{True } p = 0.6",
            font_size=30, color=YELLOW
        ).move_to(true_p_label)
        self.play(Transform(true_p_label, true_reveal))
        self.wait(1.5)
        self.play(FadeOut(c14))

        c15 = cap("Even after 1000 flips,\nwe only get an estimate.\nThe true value stays hidden.")
        self.play(FadeIn(c15))
        self.wait(3)
        self.play(FadeOut(c15))

        # --- Part D: Connect back to bandits ---
        c16 = cap("Same for bandits:\nwe see reward samples,\nnever the true means.")
        self.play(FadeIn(c16))
        self.wait(2)

        c16b = cap("So we cannot directly\nobserve our regret.")
        self.play(FadeOut(c16))
        self.play(FadeIn(c16b))
        self.wait(2.5)

        clear(coin_grp, true_p_label, flip_display, flip_symbols,
              estimate_display, c16b)

        # ============================
        # 11. SUBOPTIMALITY GAP
        # ============================
        section_title("Suboptimality Gap")

        c17 = cap("The gap measures how far\nan arm is from the best.")
        delta_eq = MathTex(
            r"\Delta_i = \mu^\star - \mu_i",
            font_size=48
        )
        self.play(Write(delta_eq), FadeIn(c17))
        self.wait(2.5)
        clear(delta_eq, c17)

        # ============================
        # 12. EXAMPLE: 3 ARMS
        # ============================
        section_title("Example: Three Arms")

        c18 = cap("Suppose three arms with\nthese true means.")
        means_eq = MathTex(
            r"\mu_1 = 0.8, \quad \mu_2 = 0.5, \quad \mu_3 = 0.7",
            font_size=38
        ).shift(UP * 1.8)
        self.play(Write(means_eq), FadeIn(c18))
        self.wait(2)

        # Bar chart
        bars = VGroup()
        bar_data = [(0.8, RED, "a_1"), (0.5, BLUE, "a_2"), (0.7, GREEN, "a_3")]
        baseline_y = -1.5
        for i, (val, col, lab) in enumerate(bar_data):
            bar = Rectangle(
                width=1.2, height=val * 3,
                fill_color=col, fill_opacity=0.5, stroke_color=col
            )
            bar.move_to(RIGHT * (i - 1) * 2)
            bar.align_to(UP * baseline_y, DOWN)
            label = MathTex(lab, font_size=28).next_to(bar, DOWN, buff=0.15)
            val_label = MathTex(str(val), font_size=24).next_to(bar, UP, buff=0.1)
            bars.add(VGroup(bar, label, val_label))

        self.play(FadeOut(c18))
        c19 = cap("The best arm is a_1\nwith mu-star = 0.8.")
        self.play(
            LaggedStart(*[GrowFromEdge(b, DOWN) for b in bars], lag_ratio=0.2),
            FadeIn(c19)
        )
        self.wait(1.5)

        star_line = DashedLine(
            start=LEFT * 3.5 + UP * (baseline_y + 0.8 * 3),
            end=RIGHT * 3.5 + UP * (baseline_y + 0.8 * 3),
            color=YELLOW, dash_length=0.15
        )
        star_label = MathTex(
            r"\mu^\star\!=\!0.8", font_size=24, color=YELLOW
        ).next_to(star_line, RIGHT, buff=0.15)
        self.play(Create(star_line), FadeIn(star_label))
        self.wait(2)
        clear(means_eq, bars, star_line, star_label, c19)

        # Deltas
        c20 = cap("Now compute the\nsuboptimality gaps.")
        delta_calc = MathTex(
            r"\Delta_1 &= 0.8 - 0.8 = 0 \\",
            r"\Delta_2 &= 0.8 - 0.5 = 0.3 \\",
            r"\Delta_3 &= 0.8 - 0.7 = 0.1",
            font_size=36
        )
        self.play(Write(delta_calc), FadeIn(c20))
        self.wait(3)
        clear(delta_calc, c20)

        # ============================
        # 13. CAN DELTA BE NEGATIVE?
        # ============================
        c21 = cap("Can the gap ever\nbe negative?")
        neg_eq = MathTex(
            r"\Delta_a = \mu^\star - \mu_a \ge 0",
            font_size=42
        ).shift(UP * 0.8)
        neg_text = Text(
            "No, because mu-star\nis the maximum mean.",
            font_size=26
        ).next_to(neg_eq, DOWN, buff=0.6)
        self.play(Write(neg_eq), FadeIn(c21))
        self.wait(1.5)
        self.play(FadeIn(neg_text, shift=UP * 0.2))
        self.wait(2)

        self.play(FadeOut(c21))
        c22 = cap("There is always at least\none arm with gap zero.")
        opt_eq = MathTex(
            r"\exists\; a^\star: \;\; \Delta_{a^\star} = 0",
            font_size=38
        ).next_to(neg_text, DOWN, buff=0.5)
        self.play(Write(opt_eq), FadeIn(c22))
        self.wait(2.5)
        clear(neg_eq, neg_text, opt_eq, c22)

        # ============================
        # 14. IS REGRET NONNEG?
        # ============================
        c23 = cap("Is regret always\nnonnegative?")
        reg_pos = MathTex(r"R_T \ge 0", font_size=48).shift(UP * 0.5)
        reg_explain = Text(
            "Yes! Each term adds a\nnonnegative contribution.\nBest case: regret is 0.",
            font_size=24, line_spacing=1.3
        ).next_to(reg_pos, DOWN, buff=0.5)
        self.play(Write(reg_pos), FadeIn(c23))
        self.wait(1.5)
        self.play(FadeIn(reg_explain, shift=UP * 0.2))
        self.wait(2.5)
        clear(reg_pos, reg_explain, c23)

        # ============================
        # 15. UPPER BOUND
        # ============================
        c24 = cap("What is an upper\nbound on regret?")
        bound_eq = MathTex(r"0 \le R_T \le T", font_size=48).shift(UP * 0.5)
        bound_text = Text(
            "Rewards are in [0,1], so\neach round's loss is at most 1.\nOver T rounds: at most T.",
            font_size=24, line_spacing=1.3
        ).next_to(bound_eq, DOWN, buff=0.5)
        self.play(Write(bound_eq), FadeIn(c24))
        self.wait(1.5)
        self.play(FadeIn(bound_text, shift=UP * 0.2))
        self.wait(3)
        clear(bound_eq, bound_text, c24)

        # ============================
        # 16. WORKED TABLE EXAMPLE
        # ============================
        section_title("Worked Example")

        c25 = cap("Let's trace regret\nround by round.")

        header = VGroup(
            MathTex(r"\text{Round}", font_size=28),
            MathTex(r"\text{Action}", font_size=28),
            MathTex(r"\text{Regret}", font_size=28),
        ).arrange(RIGHT, buff=1.5).shift(UP * 2.5)
        h_line = Line(LEFT * 4.5, RIGHT * 4.5, color=GREY).next_to(header, DOWN, buff=0.15)

        self.play(FadeIn(header), Create(h_line), FadeIn(c25))
        self.wait(1)

        table_data = [
            ("1", "a_1", "0.0", GREEN),
            ("2", "a_2", "0.3", RED),
            ("3", "a_3", "0.1", ORANGE),
            ("4", "a_1", "0.0", GREEN),
            ("5", "a_3", "0.1", ORANGE),
        ]

        rows = VGroup()
        for i, (rnd, arm, reg, col) in enumerate(table_data):
            row = VGroup(
                MathTex(rnd, font_size=28),
                MathTex(arm, font_size=28),
                MathTex(reg, font_size=28, color=col),
            ).arrange(RIGHT, buff=1.5)
            row.move_to(header).shift(DOWN * (0.55 * (i + 1) + 0.15))
            rows.add(row)

        for row in rows:
            self.play(FadeIn(row, shift=RIGHT * 0.3), run_time=0.6)
            self.wait(0.4)

        self.wait(2)
        clear(header, h_line, rows, c25)

        # ============================
        # 17. TOTAL REGRET
        # ============================
        c26 = cap("Add up the regrets\nfor total regret.")
        total_eq = MathTex(
            r"R_5 = 0.0 + 0.3 + 0.1 + 0.0 + 0.1",
            font_size=36
        ).shift(UP * 0.5)
        self.play(Write(total_eq), FadeIn(c26))
        self.wait(2)

        total_result = MathTex(
            r"= 0.5", font_size=42, color=YELLOW
        ).next_to(total_eq, DOWN, buff=0.4)
        self.play(Write(total_result))
        self.wait(2)
        clear(total_eq, total_result, c26)

        # ============================
        # 18. DECOMPOSITION VERIFICATION
        # ============================
        c27 = cap("Verify using the\ndecomposition formula.")
        decomp_check = MathTex(
            r"R_T = \sum_a n_a(T) \, \Delta_a",
            font_size=38
        ).shift(UP * 1.5)
        self.play(Write(decomp_check), FadeIn(c27))
        self.wait(1.5)

        counts = MathTex(
            r"n_1 = 2, \quad n_2 = 1, \quad n_3 = 2",
            font_size=32
        ).next_to(decomp_check, DOWN, buff=0.5)
        self.play(FadeIn(counts))
        self.wait(1)

        calc = MathTex(
            r"R_T &= 2(0) + 1(0.3) + 2(0.1) \\",
            r"&= 0 + 0.3 + 0.2 = 0.5",
            font_size=34
        ).next_to(counts, DOWN, buff=0.5)
        self.play(Write(calc))
        self.wait(1.5)

        self.play(FadeOut(c27))
        c28 = cap("Both methods give\nthe same answer!")
        check = MathTex(
            r"\checkmark", font_size=60, color=GREEN
        ).next_to(calc, RIGHT, buff=0.5)
        self.play(FadeIn(check, scale=0.5), FadeIn(c28))
        self.wait(2.5)
        clear(decomp_check, counts, calc, check, c28)

        # ============================
        # 19. SUMMARY
        # ============================
        summary_title = Text(
            "Key Takeaways", font_size=40, weight=BOLD, color=YELLOW
        ).shift(UP * 2.5)
        takeaways = VGroup(
            MathTex(r"\bullet \;\; \mathcal{A} = \{a_1, \dots, a_K\}", font_size=30),
            MathTex(r"\bullet \;\; \mu^\star = \max_i \mu_i", font_size=30),
            MathTex(r"\bullet \;\; \Delta_i = \mu^\star - \mu_i \ge 0", font_size=30),
            MathTex(r"\bullet \;\; R_T = \sum_i \Delta_i \, \mathbb{E}[n_i(T)]", font_size=30),
            MathTex(r"\bullet \;\; 0 \le R_T \le T", font_size=30),
        ).arrange(DOWN, buff=0.35, aligned_edge=LEFT).next_to(summary_title, DOWN, buff=0.5)

        self.play(FadeIn(summary_title))
        for t in takeaways:
            self.play(FadeIn(t, shift=RIGHT * 0.3), run_time=0.5)
            self.wait(0.5)
        self.wait(3)
        clear(summary_title, takeaways)

        # End
        end = Text("End of Section", font_size=44, weight=BOLD)
        self.play(FadeIn(end, scale=0.5))
        self.wait(2)
        self.play(FadeOut(end))
