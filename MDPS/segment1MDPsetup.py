from manim import (
    Scene, Text, MathTex, VGroup, Circle, Arrow, RoundedRectangle,
    SurroundingRectangle, FadeIn, FadeOut, Write,
    UP, DOWN, WHITE, BLUE, BLUE_E, YELLOW, YELLOW_E, GREEN, GREEN_E,
    smooth,
)
import numpy as np


class LayeredMDPRollout(Scene):
    """
    Layered MDP rollout with adjustable hold times:

    - State labels BELOW circles.
    - Each nonterminal state contains two tiny action-dots (stacked vertically).
    - Order per step:
        highlight state -> hold (state_hold_time)
        highlight chosen action-dot -> hold (action_hold_time)
        show reward bubble -> transition to next -> mark visited
    - Multiple episodes.

    Avoids prior Manim/NumPy/MathTex pitfalls.
    """

    # -----------------------
    # Timing knobs (tune these!)
    # -----------------------
    state_highlight_time = 0.20   # time to animate state turning yellow
    state_hold_time = 0.3        # <--- YOU asked for this: hold state highlight

    action_highlight_time = 0.5  # time to animate action-dot turning yellow
    action_hold_time = 0.3       # <--- YOU asked for this: hold action highlight

    reward_in_time = 0.25
    reward_hold_time = 0.10
    reward_slide_time = 0.18
    reward_out_time = 0.12

    next_state_highlight_time = 0.20
    visited_time = 0.14
    reset_dot_time = 0.10

    between_episode_pause = 0.20
    banner_in_time = 0.22
    banner_hold_time = 0.10
    banner_out_time = 0.18

    # -----------------------
    # Other knobs
    # -----------------------
    seed = 2
    episodes = 3
    max_steps_per_episode = 8

    actions_tex = [r"a_1", r"a_2"]  # action indices 0/1

    reward_sigma = 0.12

    # -------- visuals helpers --------
    def make_layer_outline(
        self,
        objects: VGroup,
        label: str,
        buff: float = 0.70,
        corner_radius: float = 0.45,
        stroke_width: float = 2.0,
        opacity: float = 0.33,
    ) -> VGroup:
        outline = SurroundingRectangle(
            objects,
            buff=buff,
            corner_radius=corner_radius,
            stroke_width=stroke_width,
            color=WHITE,
        ).set_opacity(opacity)

        layer_label = (
            Text(label, font_size=22)
            .next_to(outline, DOWN, buff=0.22)
            .set_opacity(opacity + 0.10)
        )

        g = VGroup(outline, layer_label)
        g.set_z_index(-2)
        return g

    # -------- MDP model --------
    def reward_mean(self, s: str, a: int, sp: str) -> float:
        base = -0.05
        if sp == "sT":
            base += 1.0
        # mild shaping
        if s == "s0" and a == 0 and sp == "s1T":
            base += 0.10
        if s == "s0" and a == 1 and sp == "s1B":
            base += 0.10
        if s in ["s1T", "s1B"] and a == 0 and sp == "s2T":
            base += 0.08
        if s in ["s1T", "s1B"] and a == 1 and sp == "s2B":
            base += 0.08
        return base

    def choose_action(self, s: str, t: int, ep: int) -> int:
        return np.random.randint(0, len(self.actions_tex))

    def build_transition_kernel(self):
        P = {}
        # layer0 -> layer1
        P[("s0", 0)] = [("s1T", 0.80), ("s1B", 0.20)]
        P[("s0", 1)] = [("s1T", 0.20), ("s1B", 0.80)]
        # layer1 -> layer2
        for s1 in ["s1T", "s1B"]:
            P[(s1, 0)] = [("s2T", 0.75), ("s2B", 0.25)]
            P[(s1, 1)] = [("s2T", 0.25), ("s2B", 0.75)]
        # layer2 -> terminal (with some chance to stick)
        for s2 in ["s2T", "s2B"]:
            P[(s2, 0)] = [("sT", 0.85), (s2, 0.15)]
            P[(s2, 1)] = [("sT", 0.70), (s2, 0.30)]
        return P

    def sample_next_state(self, P, s: str, a: int) -> str:
        dist = P[(s, a)]
        states = [x for x, _ in dist]
        probs = [p for _, p in dist]
        idx = np.random.choice(len(states), p=probs)
        return states[idx]

    # -------- layout --------
    def layered_positions(self):
        x0, x1, x2, x3 = -5.0, -1.7, 1.7, 5.0
        y_top, y_bot = 1.4, -1.4
        return {
            "s0":  np.array([x0, 0.0, 0.0]),
            "s1T": np.array([x1, y_top, 0.0]),
            "s1B": np.array([x1, y_bot, 0.0]),
            "s2T": np.array([x2, y_top, 0.0]),
            "s2B": np.array([x2, y_bot, 0.0]),
            "sT":  np.array([x3, 0.0, 0.0]),
        }

    def construct(self):
        np.random.seed(self.seed)

        P = self.build_transition_kernel()
        pos = self.layered_positions()

        header = Text("Layered MDP Rollout", font_size=40).to_edge(UP)
        self.play(FadeIn(header))

        label_tex = {
            "s0":  r"s_{\mathrm{start}}",
            "s1T": r"s^{(1)}_{1}",
            "s1B": r"s^{(1)}_{2}",
            "s2T": r"s^{(2)}_{1}",
            "s2B": r"s^{(2)}_{2}",
            "sT":  r"s_{\mathrm{final}}",
        }

        # ---- nodes (circle + label BELOW) ----
        radius = 0.42
        nodes = {}
        labels = {}

        for name, p in pos.items():
            opacity = 0.25 if name != "sT" else 0.18
            c = (
                Circle(radius=radius)
                .set_fill(BLUE, opacity=opacity)
                .set_stroke(BLUE_E, width=2)
                .move_to(p)
            )
            t = MathTex(label_tex[name], font_size=30).set_opacity(0.9)
            t.next_to(c, DOWN, buff=0.18)

            nodes[name] = c
            labels[name] = t

        node_group = VGroup(*(nodes[k] for k in ["s0", "s1T", "s1B", "s2T", "s2B", "sT"]))
        label_group = VGroup(*(labels[k] for k in ["s0", "s1T", "s1B", "s2T", "s2B", "sT"]))

        # ---- action dots inside each nonterminal state ----
        action_dots = {}  # state_name -> [dot0(top), dot1(bottom)]
        dot_r = 0.07
        dot_off = 0.12
        for name in ["s0", "s1T", "s1B", "s2T", "s2B"]:
            center = nodes[name].get_center()
            dot0 = Circle(radius=dot_r).set_fill(WHITE, opacity=0.35).set_stroke(WHITE, opacity=0.0, width=0)
            dot1 = Circle(radius=dot_r).set_fill(WHITE, opacity=0.35).set_stroke(WHITE, opacity=0.0, width=0)
            dot0.move_to(center + UP * dot_off)
            dot1.move_to(center + DOWN * dot_off)
            action_dots[name] = [dot0, dot1]

        dots_group = VGroup(*[d for st in action_dots for d in action_dots[st]])

        # ---- layers ----
        layer0 = VGroup(nodes["s0"])
        layer1 = VGroup(nodes["s1T"], nodes["s1B"])
        layer2 = VGroup(nodes["s2T"], nodes["s2B"])
        layer3 = VGroup(nodes["sT"])

        layer0_box = self.make_layer_outline(layer0, "Layer 0")
        layer1_box = self.make_layer_outline(layer1, "Layer 1")
        layer2_box = self.make_layer_outline(layer2, "Layer 2")
        layer3_box = self.make_layer_outline(layer3, "Terminal")
        layer3_box[0].set_opacity(0.25)

        # ---- edges ----
        def edge(u, v, opacity=0.45):
            return Arrow(
                nodes[u].get_center(),
                nodes[v].get_center(),
                buff=0.52,
                stroke_width=3,
                max_tip_length_to_length_ratio=0.12,
            ).set_opacity(opacity)

        edges = VGroup(
            edge("s0", "s1T"), edge("s0", "s1B"),
            edge("s1T", "s2T"), edge("s1T", "s2B"),
            edge("s1B", "s2T"), edge("s1B", "s2B"),
            edge("s2T", "sT"), edge("s2B", "sT"),
        )

        # intro
        self.play(
            FadeIn(layer0_box), FadeIn(layer1_box), FadeIn(layer2_box), FadeIn(layer3_box),
            FadeIn(edges),
            FadeIn(node_group),
            FadeIn(dots_group),
            Write(label_group),
        )

        terminal_note = Text("terminal (no actions)", font_size=22).next_to(nodes["sT"], DOWN, buff=0.55)
        self.play(FadeIn(terminal_note, shift=DOWN * 0.1), run_time=0.35)

        # -------- animation helpers (return Animation; do NOT self.play inside) --------
        def current_state_anim(name: str):
            return nodes[name].animate.set_fill(YELLOW, opacity=0.9).set_stroke(YELLOW_E, width=3)

        def next_state_anim(name: str):
            return nodes[name].animate.set_fill(YELLOW, opacity=0.9).set_stroke(YELLOW_E, width=3)

        def visited_state_anim(name: str):
            return nodes[name].animate.set_fill(GREEN, opacity=0.35).set_stroke(GREEN_E, width=2)

        def base_state_anim(name: str):
            base_op = 0.25 if name != "sT" else 0.18
            return nodes[name].animate.set_fill(BLUE, opacity=base_op).set_stroke(BLUE_E, width=2)

        def reset_all_states_anims():
            return [base_state_anim(n) for n in ["s0", "s1T", "s1B", "s2T", "s2B", "sT"]]

        def reset_all_dots_anims():
            anims = []
            for st in ["s0", "s1T", "s1B", "s2T", "s2B"]:
                anims.append(action_dots[st][0].animate.set_fill(WHITE, opacity=0.35))
                anims.append(action_dots[st][1].animate.set_fill(WHITE, opacity=0.35))
            return anims

        def highlight_dot_anim(st: str, a: int):
            return action_dots[st][a].animate.set_fill(YELLOW, opacity=1.0)

        # -------- run episodes --------
        for ep in range(1, self.episodes + 1):
            ep_banner = Text(f"Episode {ep}", font_size=28).next_to(header, DOWN, buff=0.9)
            self.play(FadeIn(ep_banner), run_time=self.banner_in_time)
            self.wait(self.banner_hold_time)
            self.play(FadeOut(ep_banner), run_time=self.banner_out_time)

            # reset
            self.play(*reset_all_dots_anims(), run_time=0.15)
            self.play(*reset_all_states_anims(), run_time=0.30)

            s = "s0"
            self.play(current_state_anim(s), run_time=self.state_highlight_time)

            for t in range(1, self.max_steps_per_episode + 1):
                if s == "sT":
                    break

                # hold current state's highlight
                self.wait(self.state_hold_time)

                a = self.choose_action(s, t, ep)

                # highlight chosen action dot, then hold it
                self.play(highlight_dot_anim(s, a), run_time=self.action_highlight_time)
                self.wait(self.action_hold_time)

                sp = self.sample_next_state(P, s, a)
                r = np.random.normal(self.reward_mean(s, a, sp), self.reward_sigma)

                # reward bubble
                center = nodes[s].get_center()
                reward_text = Text(f"r = {r:+.3f}", font_size=28).move_to(center + UP * 0.95)
                bubble = (
                    RoundedRectangle(corner_radius=0.12, width=2.1, height=0.62)
                    .set_fill(WHITE, opacity=0.15)
                    .set_stroke(WHITE, opacity=0.45, width=1)
                    .move_to(reward_text.get_center())
                )

                self.play(FadeIn(bubble, scale=0.95), FadeIn(reward_text, shift=UP * 0.12), run_time=self.reward_in_time)
                self.wait(self.reward_hold_time)
                self.play(
                    reward_text.animate.shift(UP * 0.45),
                    bubble.animate.shift(UP * 0.45).set_opacity(0.05),
                    rate_func=smooth,
                    run_time=self.reward_slide_time
                )
                self.play(FadeOut(reward_text), FadeOut(bubble), run_time=self.reward_out_time)

                # go to next state, then mark previous visited
                self.play(next_state_anim(sp), run_time=self.next_state_highlight_time)
                self.play(visited_state_anim(s), run_time=self.visited_time)

                # reset dots on the state we just left (so next time it's clean)
                self.play(
                    action_dots[s][0].animate.set_fill(WHITE, opacity=0.35),
                    action_dots[s][1].animate.set_fill(WHITE, opacity=0.35),
                    run_time=self.reset_dot_time
                )

                s = sp

            self.wait(self.between_episode_pause)

        # outro
        self.play(
            FadeOut(terminal_note),
            FadeOut(layer0_box), FadeOut(layer1_box), FadeOut(layer2_box), FadeOut(layer3_box),
            FadeOut(edges),
            FadeOut(dots_group),
            FadeOut(label_group),
            FadeOut(node_group),
            FadeOut(header),
            run_time=0.8
        )
        self.wait(0.2)
