from manim import *
import numpy as np

class Test(Scene):
    def construct(self):

        title = Tex(r"\textbf{UCB Algorithm: Worked Example}", color=YELLOW)
        title.to_edge(UP)
        self.play(Write(title))

        # UCB Formula
        formula = MathTex(
            r"""
            \mathrm{UCB}_a(t)=
            \begin{cases}
            \hat{\mu}_a(t)+\sqrt{\frac{4\log T}{n_a(t)}} & \text{if } n_a(t)>0 \\
            \infty & \text{if } n_a(t)=0
            \end{cases}
            """
        )
        formula.scale(0.7)
        formula.next_to(title, DOWN)
        self.play(Write(formula))

        # Table header
        headers = ["Round", "UCB Values $(a_1,a_2)$", "Action", "Reward"]
        table_data = [
            ["1", "", "", ""],
            ["2", "", "", ""],
            ["3", "", "", ""],
            ["4", "", "", ""],
            ["5", "", "", ""],
        ]

        table = Table(
            table_data,
            col_labels=[Tex(h) for h in headers],
            include_outer_lines=True,
            element_to_mobject=Tex,
        )
        table.scale(0.6)
        table.next_to(formula, DOWN, buff=0.6)

        '''
        table.add_highlighted_cell((1, 1), color=BLUE).set_opacity(0.5)
        table.add_highlighted_cell((1, 2), color=BLUE).set_opacity(0.5)
        table.add_highlighted_cell((1, 3), color=BLUE).set_opacity(0.5)
        table.add_highlighted_cell((1, 4), color=BLUE).set_opacity(0.5)
        
        col_labels = table.get_col_labels()
        col_labels[0].set_color_by_gradient(PURE_GREEN, BLUE)
        col_labels[1].set_color_by_gradient(PURE_GREEN, BLUE)
        col_labels[2].set_color_by_gradient(PURE_GREEN, BLUE)
        col_labels[3].set_color_by_gradient(PURE_GREEN, BLUE)
        '''

        # --- Draw order: lines -> column labels -> round numbers ---
        table.get_vertical_lines().set_opacity(0)
        table.get_horizontal_lines().set_opacity(0)
        table.get_labels().set_opacity(0)  # includes col labels
        table.get_entries_without_labels().set_opacity(0)  # body entries
        self.add(table)

        lines = VGroup(table.get_vertical_lines(), table.get_horizontal_lines())
        self.play(Create(lines.set_opacity(1)))
        self.play(Write(table.get_col_labels().set_opacity(1)))

        n_rows = len(table_data)
        round_entries = VGroup(*[
            table.get_entries_without_labels((r, 1)) for r in range(1, n_rows + 1)
        ])
        self.play(Write(round_entries.set_opacity(1)))

        # Make the rest of the body entries available (they're empty anyway, but this
        # ensures later Transform() calls will show up)
        table.get_entries_without_labels().set_opacity(1)

        # Helper: highlight a row
        def highlight_row(row_index):
            return table.get_rows()[row_index].animate.set_fill(YELLOW, opacity=0.8)
        
        # Round-by-round updates
        updates = [
            r"(\infty,\infty)",
            r"(2.3721,\infty)",
            r"(2.3721, 1.9721)",
            r"(1.7823, 1.9721)",
            r"(1.7823, 1.3323)",
        ]

        ucb_updates_a1 = [
            r"\infty",
            r"\frac{0.7}{1}+\sqrt{\frac{4\log 5}{1}}",
            r"\frac{0.7}{1}+\sqrt{\frac{4\log 5}{1}}",
            r"\frac{0.7 + 0.5}{2}+\sqrt{\frac{4\log 5}{2}}",
            r"\frac{0.7 + 0.5}{2}+\sqrt{\frac{4\log 5}{2}}",
        ]

        ucb_updates_a2 = [
            r"\infty",
            r"\infty",
            r"\frac{0.3}{1}+\sqrt{\frac{4\log 5}{1}}",
            r"\frac{0.3}{1}+\sqrt{\frac{4\log 5}{1}}",
            r"\frac{0.3 + 0.0}{2}+\sqrt{\frac{4\log 5}{2}}",
        ]

        actions = [r"a_1", r"a_2", r"a_1", r"a_2", r"a_1"]
        rewards = [r"0.7", r"0.3", r"0.5", r"0.0", None]

        ucb_a1 = MathTex(
            r"\mathrm{UCB}_{a_1}(t) = \hat{\mu}_{a_1}(t) + \sqrt{\frac{4 \log T}{n_{a_1}(t)}}"
        ).scale(0.75).move_to(formula.get_center()).shift(LEFT*3)
        ucb_a2 = MathTex(
            r"\mathrm{UCB}_{a_2}(t) = \hat{\mu}_{a_2}(t) + \sqrt{\frac{4 \log T}{n_{a_2}(t)}}"
        ).scale(0.75).move_to(formula.get_center()).shift(RIGHT*3)

        self.play(ReplacementTransform(formula, VGroup(ucb_a1, ucb_a2)))

        for i in range(5):

            # Highlight the current round in the table
            self.play(highlight_row(i + 1))  
            self.wait(0.5)

            # Update the UCB formula with current round's values
            current_a1 = MathTex(
                r"\mathrm{UCB}_{a_{1}}(" + str(i + 1) + r") = " + ucb_updates_a1[i]
            ).scale(0.75).move_to(formula.get_center()).shift(LEFT*3)
            current_a2 = MathTex(
                r"\mathrm{UCB}_{a_{2}}(" + str(i + 1) + r") = " + ucb_updates_a2[i]
            ).scale(0.75).move_to(formula.get_center()).shift(RIGHT*3)

            self.play(Transform(ucb_a1, current_a1), Transform(ucb_a2, current_a2))
            self.wait(0.5)

            # Fill UCB index
            ucb_cell = table.get_cell((i + 2, 2))
            new_ucb = MathTex(updates[i]).scale(0.7)
            new_ucb.move_to(ucb_cell)

            self.play(ReplacementTransform(VGroup(current_a1, current_a2), new_ucb))
            
            # Since transforms mutate object, set current_a1 and current_a2 back to 
            # original values 
            current_a1 = MathTex(
                r"\mathrm{UCB}_{a_{1}}(" + str(i + 1) + r") = " + ucb_updates_a1[i]
            ).scale(0.75).move_to(formula.get_center()).shift(LEFT*3)
            current_a2 = MathTex(
                r"\mathrm{UCB}_{a_{2}}(" + str(i + 1) + r") = " + ucb_updates_a2[i]
            ).scale(0.75).move_to(formula.get_center()).shift(RIGHT*3)

            # Indicate which UCB value is greater
            if actions[i] == "a_1":
                self.play(Indicate(ucb_a1, color=RED))

                # Fill action
                action_cell = table.get_cell((i + 2, 3))
                new_action = MathTex(actions[i]).scale(0.7).move_to(action_cell)
                self.play(ReplacementTransform(
                    current_a1, new_action
                ))
            else:
                self.play(Indicate(ucb_a2, color=RED))

                # Fill action
                action_cell = table.get_cell((i + 2, 3))
                new_action = MathTex(actions[i]).scale(0.7).move_to(action_cell)
                self.play(ReplacementTransform(
                    current_a2, new_action
                ))

            self.wait(0.2)

            # Fill reward
            if rewards[i] is not None:
                reward_cell = table.get_cell((i + 2, 4))
                new_reward = MathTex(rewards[i]).scale(0.8)
                new_reward.move_to(reward_cell)

                self.play(Transform(reward_cell, new_reward))
                self.wait(0.4)

        self.wait(3)