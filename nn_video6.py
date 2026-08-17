from manim import *
import numpy as np

# ── palette ──────────────────────────────────────────────────────
INPUT_COL   = BLUE
HIDDEN_COL  = GREEN
OUTPUT_COL  = RED
ACCENT      = YELLOW
WEIGHT_COL  = GREY_B
W_COL       = TEAL          # weight annotations & highlights
B_COL       = "#e88dcd"     # bias annotations & highlights (pink)
RELU_COL    = ORANGE
BG          = "#1a1a2e"
CALC_BG     = "#0d0d1a"

def caption(text, max_words=6):
    words = text.split()
    lines = []
    for i in range(0, len(words), max_words):
        lines.append(" ".join(words[i:i + max_words]))
    return "\n".join(lines)

def make_caption(text, max_words=6):
    t = Text(caption(text, max_words), font_size=28, color=WHITE)
    t.to_edge(DOWN, buff=0.4)
    return t


class FeedforwardNN(MovingCameraScene):
    def construct(self):
        self.camera.background_color = BG

        # ═══════════════════════════════════════════════
        # PART 1 – TITLE
        # ═══════════════════════════════════════════════
        title = Text("Feedforward Neural Networks", font_size=48, color=WHITE)
        self.play(Write(title), run_time=1.5)
        self.wait(1.5)
        self.play(FadeOut(title))
        self.wait(0.3)

        # ═══════════════════════════════════════════════
        # PART 1b – WHAT A NN IS
        # ═══════════════════════════════════════════════
        idea_title = Text("The Big Idea", font_size=40, color=ACCENT)
        idea_title.to_edge(UP, buff=0.5)
        self.play(Write(idea_title))

        cap_idea1 = make_caption(
            "We have data points (x, y) and want a function that fits them."
        )
        self.play(FadeIn(cap_idea1))

        line1 = MathTex(
            r"\text{Data: } \{(x_i, y_i)\}_{i=1}^{n}",
            font_size=34
        ).shift(UP * 1.0)
        line2 = MathTex(
            r"\text{Goal: find } \hat{f} : \mathbb{R}^m \to \mathbb{R}^n"
            r"\text{ that fits the data}",
            font_size=32
        ).next_to(line1, DOWN, buff=0.5)
        self.play(Write(line1), run_time=1)
        self.play(Write(line2), run_time=1)
        self.wait(2)

        self.play(FadeOut(cap_idea1))
        cap_idea2 = make_caption(
            "Training learns the weights. Once fixed, the NN is just a function."
        )
        self.play(FadeIn(cap_idea2))

        line3 = MathTex(
            r"\text{Training } \longrightarrow"
            r"\text{ choose weights } W, b",
            font_size=32
        ).next_to(line2, DOWN, buff=0.5)
        line4 = MathTex(
            r"\text{After training: } \hat{f}(x) = "
            r"\text{fixed function } \mathbb{R}^m \to \mathbb{R}^n",
            font_size=30
        ).next_to(line3, DOWN, buff=0.4)
        self.play(Write(line3), run_time=1)
        self.play(Write(line4), run_time=1)
        self.wait(2.5)

        self.play(*[FadeOut(m) for m in
                     [idea_title, line1, line2, line3, line4, cap_idea2]])
        self.wait(0.3)

        # ═══════════════════════════════════════════════
        # PART 2 – BUILDING BLOCKS
        # ═══════════════════════════════════════════════
        bb_title = Text("Two Building Blocks", font_size=40, color=ACCENT)
        bb_title.to_edge(UP, buff=0.5)
        self.play(Write(bb_title))

        box1 = RoundedRectangle(
            corner_radius=0.15, width=5, height=1.8,
            stroke_color=INPUT_COL, fill_color=INPUT_COL, fill_opacity=0.15
        ).shift(LEFT * 3 + DOWN * 0.3)
        lbl1_title = Text("Affine Map", font_size=26, color=INPUT_COL)
        lbl1_eq = MathTex(r"z = Wx + b", font_size=32)
        lbl1_title.next_to(box1.get_top(), DOWN, buff=0.25)
        lbl1_eq.next_to(lbl1_title, DOWN, buff=0.2)

        box2 = RoundedRectangle(
            corner_radius=0.15, width=5, height=1.8,
            stroke_color=HIDDEN_COL, fill_color=HIDDEN_COL, fill_opacity=0.15
        ).shift(RIGHT * 3 + DOWN * 0.3)
        lbl2_title = Text("Nonlinear Activation", font_size=26, color=HIDDEN_COL)
        lbl2_eq = MathTex(r"\sigma(z) = \max\{0, z\}", font_size=32)
        lbl2_title.next_to(box2.get_top(), DOWN, buff=0.25)
        lbl2_eq.next_to(lbl2_title, DOWN, buff=0.2)

        cap1 = make_caption(
            "A neural network layer combines an affine map with a nonlinear activation."
        )
        self.play(
            FadeIn(box1), Write(lbl1_title), Write(lbl1_eq),
            FadeIn(box2), Write(lbl2_title), Write(lbl2_eq),
            FadeIn(cap1), run_time=2
        )
        self.wait(2)

        arr = Arrow(box1.get_right(), box2.get_left(), buff=0.15, color=WHITE)
        then_lbl = Text("then", font_size=22, color=GREY_B).next_to(arr, UP, buff=0.1)
        self.play(GrowArrow(arr), FadeIn(then_lbl))
        self.wait(1)

        layer_eq = MathTex(
            r"h^{(\ell)} = \sigma\!\bigl(W^{(\ell)} h^{(\ell-1)} + b^{(\ell)}\bigr)",
            font_size=36
        ).shift(DOWN * 2.2)
        cap2 = make_caption(
            "Each layer applies this formula. Stack several to get a deep network."
        )
        self.play(FadeOut(cap1), Write(layer_eq), FadeIn(cap2), run_time=1.5)
        self.wait(2.5)

        self.play(*[FadeOut(m) for m in [
            bb_title, box1, box2, lbl1_title, lbl1_eq,
            lbl2_title, lbl2_eq, arr, then_lbl, layer_eq, cap2
        ]])
        self.wait(0.3)

        # ═══════════════════════════════════════════════
        # PART 3 – BUILD THE 2-3-3-2 NETWORK
        # ═══════════════════════════════════════════════
        net_title = Text("A 2-3-3-2 Network", font_size=40, color=ACCENT)
        net_title.to_edge(UP, buff=0.4)
        self.play(Write(net_title))

        layers_spec = [2, 3, 3, 2]
        layer_names = ["Input", "Hidden 1", "Hidden 2", "Output"]
        layer_colors = [INPUT_COL, HIDDEN_COL, HIDDEN_COL, OUTPUT_COL]
        x_positions = [-4.5, -1.5, 1.5, 4.5]
        neuron_radius = 0.35

        neurons = []
        for l_idx, (n_count, x_pos) in enumerate(zip(layers_spec, x_positions)):
            layer_neurons = []
            y_offsets = np.linspace(
                (n_count - 1) * 1.1 / 2,
                -(n_count - 1) * 1.1 / 2,
                n_count,
            )
            for n_idx, y_off in enumerate(y_offsets):
                c = Circle(
                    radius=neuron_radius,
                    stroke_color=layer_colors[l_idx],
                    fill_color=layer_colors[l_idx],
                    fill_opacity=0.25, stroke_width=2.5,
                ).move_to([x_pos, y_off, 0])
                layer_neurons.append(c)
            neurons.append(layer_neurons)

        all_neuron_mobs = VGroup(*[n for layer in neurons for n in layer])
        self.play(LaggedStart(
            *[FadeIn(n, scale=0.5) for n in all_neuron_mobs],
            lag_ratio=0.05,
        ), run_time=1.5)

        # Edges grouped by target layer
        edges_by_layer = {}
        all_edges_list = []
        for l_idx in range(len(layers_spec) - 1):
            target = l_idx + 1
            edges_by_layer[target] = []
            for n_from in neurons[l_idx]:
                for n_to in neurons[target]:
                    edge = Line(
                        n_from.get_right(), n_to.get_left(),
                        stroke_color=WEIGHT_COL, stroke_width=1.2,
                        stroke_opacity=0.5,
                    )
                    edges_by_layer[target].append(edge)
                    all_edges_list.append(edge)
        all_edges = VGroup(*all_edges_list)
        self.play(LaggedStart(
            *[Create(e) for e in all_edges_list], lag_ratio=0.01,
        ), run_time=1.5)

        # Layer name labels
        layer_labels = []
        for l_idx, (name, x_pos) in enumerate(zip(layer_names, x_positions)):
            lbl = Text(name, font_size=20, color=layer_colors[l_idx])
            lbl.move_to([x_pos, -2.5, 0])
            layer_labels.append(lbl)
        ll_group = VGroup(*layer_labels)
        self.play(FadeIn(ll_group))

        # Neuron symbol labels
        input_ltex = [r"x_1", r"x_2"]
        output_ltex = [r"\hat{y}_1", r"\hat{y}_2"]
        h1_ltex = [r"h^{(1)}_1", r"h^{(1)}_2", r"h^{(1)}_3"]
        h2_ltex = [r"h^{(2)}_1", r"h^{(2)}_2", r"h^{(2)}_3"]
        all_ltex = [input_ltex, h1_ltex, h2_ltex, output_ltex]

        all_neuron_labels = []
        for layer_idx in range(4):
            for n_idx, ltex in enumerate(all_ltex[layer_idx]):
                lbl = MathTex(ltex, font_size=22, color=WHITE)
                lbl.move_to(neurons[layer_idx][n_idx].get_center())
                all_neuron_labels.append(lbl)
        nl_group = VGroup(*all_neuron_labels)
        self.play(FadeIn(nl_group))

        cap3 = make_caption(
            "This network maps 2D input to 2D output through two hidden layers."
        )
        self.play(FadeIn(cap3))
        self.wait(2)
        self.play(FadeOut(cap3))

        # ═══════════════════════════════════════════════
        # PART 3b – SHOW WEIGHTS & BIASES
        # ═══════════════════════════════════════════════
        W1 = np.array([[1, -2], [0.5, 1], [-1, 0]])
        b1 = np.array([0.1, 0.2, -0.3])
        W2 = np.array([[1, 0, -1], [0, 2, 0.5], [-0.5, 0, 1]])
        b2 = np.array([0, 0.1, -0.2])
        W3 = np.array([[1, -1, 0.5], [-0.5, 1, 1]])
        b3 = np.array([0.1, -0.1])

        Ws = [None, W1, W2, W3]
        bs = [None, b1, b2, b3]

        # Clean LaTeX annotations (no \! spacing hacks)
        wb_annot_w_str = {
            1: [r"w=(1,-2)", r"w=(0.5, 1)", r"w=(-1, 0)"],
            2: [r"w=(1,0,-1)", r"w=(0,2,0.5)", r"w=(-0.5,0,1)"],
            3: [r"w=(1,-1,0.5)", r"w=(-0.5,1,1)"],
        }
        wb_annot_b_str = {
            1: [r"b=0.1", r"b=0.2", r"b=-0.3"],
            2: [r"b=0", r"b=0.1", r"b=-0.2"],
            3: [r"b=0.1", r"b=-0.1"],
        }

        # Build annotation mobjects: wb_annots[layer][node] = VGroup(w_tex, b_tex)
        wb_annots = {}
        wb_annots_flat = []
        for l_idx in [1, 2, 3]:
            wb_annots[l_idx] = []
            for n_idx in range(layers_spec[l_idx]):
                w_tex = MathTex(
                    wb_annot_w_str[l_idx][n_idx], font_size=15, color=W_COL
                )
                b_tex = MathTex(
                    wb_annot_b_str[l_idx][n_idx], font_size=15, color=B_COL
                )
                annot = VGroup(w_tex, b_tex).arrange(DOWN, buff=0.06)
                annot.next_to(neurons[l_idx][n_idx], DOWN, buff=0.18)
                wb_annots[l_idx].append(annot)
                wb_annots_flat.append(annot)

        wb_group = VGroup(*wb_annots_flat)

        cap_wb = make_caption(
            "Here are the weights and biases for every neuron."
        )
        self.play(FadeIn(cap_wb))
        self.play(
            LaggedStart(
                *[FadeIn(a, shift=UP * 0.1) for a in wb_annots_flat],
                lag_ratio=0.06,
            ),
            run_time=2,
        )
        self.wait(3)
        self.play(FadeOut(cap_wb))

        # ═══════════════════════════════════════════════
        # PART 4 – FORWARD PASS WITH ZOOM
        # ═══════════════════════════════════════════════
        input_vals = np.array([1.0, -1.0])

        def relu(z):
            return np.maximum(0, z)

        z1 = W1 @ input_vals + b1;  h1 = relu(z1)
        z2 = W2 @ h1 + b2;          h2 = relu(z2)
        y_hat = W3 @ h2 + b3

        all_vals = [input_vals, h1, h2, y_hat]
        all_z = [None, z1, z2, None]
        has_relu = [False, True, True, False]

        value_labels = {}

        # ── Show input values ──
        cap4 = make_caption("Feed in x = (1, -1).")
        self.play(FadeIn(cap4))

        for n_idx, n in enumerate(neurons[0]):
            vstr = f"{input_vals[n_idx]:.0f}"
            vl = Text(vstr, font_size=18, color=ACCENT)
            vl.next_to(n, UP, buff=0.12)
            value_labels[(0, n_idx)] = vl
            self.play(
                n.animate.set_fill(ACCENT, opacity=0.5),
                FadeIn(vl), run_time=0.5,
            )
        self.wait(1)
        self.play(FadeOut(cap4))

        default_frame_width = self.camera.frame.width
        default_frame_center = self.camera.frame.get_center().copy()

        prev_input_syms = {
            1: [r"x_1", r"x_2"],
            2: [r"h^{(1)}_1", r"h^{(1)}_2", r"h^{(1)}_3"],
            3: [r"h^{(2)}_1", r"h^{(2)}_2", r"h^{(2)}_3"],
        }
        prev_vals_list = {1: input_vals, 2: h1, 3: h2}
        node_syms = {1: h1_ltex, 2: h2_ltex, 3: output_ltex}

        def get_incoming_edges(cur_layer, cur_node):
            elist = edges_by_layer[cur_layer]
            return [elist[i] for i in range(len(elist))
                    if i % layers_spec[cur_layer] == cur_node]

        def get_others(cur_layer, cur_node):
            others = []
            others.append(net_title)
            others.append(ll_group)
            # All wb annotations EXCEPT the current node's
            for li in wb_annots:
                for ni, annot in enumerate(wb_annots[li]):
                    if li == cur_layer and ni == cur_node:
                        continue
                    others.append(annot)
            for lbl in all_neuron_labels:
                others.append(lbl)
            for li in range(len(layers_spec)):
                for ni, n in enumerate(neurons[li]):
                    if li == cur_layer and ni == cur_node:
                        continue
                    if li == cur_layer - 1:
                        continue
                    others.append(n)
            for tgt, elist in edges_by_layer.items():
                if tgt != cur_layer:
                    for e in elist:
                        others.append(e)
                else:
                    for idx, e in enumerate(elist):
                        if idx % layers_spec[cur_layer] != cur_node:
                            others.append(e)
            for key, vl in value_labels.items():
                li, ni = key
                if li == cur_layer - 1:
                    continue
                others.append(vl)
            return VGroup(*others)

        for l_idx in range(1, 4):
            n_count = layers_spec[l_idx]
            prev_n = layers_spec[l_idx - 1]
            is_relu = has_relu[l_idx]

            if l_idx == 1:
                lc = "Computing Hidden Layer 1."
            elif l_idx == 2:
                lc = "Now Hidden Layer 2, using outputs from Layer 1."
            else:
                lc = "Finally the Output Layer. No activation here."
            layer_cap = make_caption(lc)
            self.play(FadeIn(layer_cap))
            self.wait(1.2)
            self.play(FadeOut(layer_cap))

            for n_idx in range(n_count):
                node_center = neurons[l_idx][n_idx].get_center()
                mid_x = (neurons[l_idx - 1][0].get_center()[0] + node_center[0]) / 2
                mid_y = node_center[1]
                cam_target = np.array([mid_x, mid_y, 0])

                others = get_others(l_idx, n_idx)
                incoming = get_incoming_edges(l_idx, n_idx)

                # ── Fade others, zoom in ──
                edge_anims = [
                    e.animate.set_stroke(ACCENT, width=2, opacity=1)
                    for e in incoming
                ]
                self.play(
                    others.animate.set_opacity(0.07),
                    self.camera.frame.animate.set_width(6).move_to(cam_target),
                    neurons[l_idx][n_idx].animate.set_stroke(ACCENT, width=4),
                    *edge_anims,
                    run_time=0.7,
                )

                # ── Prepare the equation data ──
                cur_annot = wb_annots[l_idx][n_idx]

                inp_syms = prev_input_syms[l_idx]
                inp_vals_arr = prev_vals_list[l_idx]
                z_val = (all_z[l_idx][n_idx]
                         if all_z[l_idx] is not None
                         else all_vals[l_idx][n_idx])
                act_val = all_vals[l_idx][n_idx]
                bias_num = bs[l_idx][n_idx]

                # Line 1 (symbolic): z = (w1)(x1) + (w2)(x2) + (b)
                parts = []
                for k in range(prev_n):
                    w_num = Ws[l_idx][n_idx, k]
                    parts.append(f"({w_num:g})({inp_syms[k]})")
                sym_line = r"z = " + " + ".join(parts) + f" + ({bias_num:g})"

                # Line 2 (numeric): = products + bias = z
                num_parts = []
                for k in range(prev_n):
                    w_num = Ws[l_idx][n_idx, k]
                    v_num = inp_vals_arr[k]
                    prod = w_num * v_num
                    num_parts.append(f"{prod:g}")
                num_parts.append(f"{bias_num:g}")
                raw_num = " + ".join(num_parts).replace("+ -", "- ")
                num_line = r"= " + raw_num + f" = {z_val:g}"

                # Line 3 (activation)
                if is_relu:
                    act_tex = MathTex(
                        r"\sigma(" + f"{z_val:g}" + r") = " + f"{act_val:g}",
                        font_size=18, color=RELU_COL,
                    )
                else:
                    act_tex = MathTex(
                        node_syms[l_idx][n_idx] + r" = " + f"{act_val:g}",
                        font_size=18, color=ACCENT,
                    )

                # ── Build equation line 1 and position it ──
                eq_line1 = MathTex(sym_line, font_size=17)
                eq_target_center = node_center + DOWN * 1.0
                eq_line1.move_to(eq_target_center)

                # ── Animate: w and b copies fly from annotation into equation ──
                # Copies start at the annotation positions; originals stay visible
                w_copy = cur_annot[0].copy().set_color(W_COL)
                b_copy = cur_annot[1].copy().set_color(B_COL)
                self.add(w_copy, b_copy)

                # Transform copies into the equation line
                self.play(
                    ReplacementTransform(
                        VGroup(w_copy, b_copy), eq_line1
                    ),
                    run_time=1.0,
                )
                self.wait(0.3)

                # ── Build remaining lines below ──
                eq_line2 = MathTex(num_line, font_size=17)
                eq_line2.next_to(eq_line1, DOWN, aligned_edge=LEFT, buff=0.1)
                act_tex.next_to(eq_line2, DOWN, aligned_edge=LEFT, buff=0.1)

                # Background box around all three lines
                all_calc = VGroup(eq_line1, eq_line2, act_tex)
                calc_bg = SurroundingRectangle(
                    all_calc, buff=0.12,
                    stroke_color=ACCENT, stroke_width=1.2,
                    fill_color=CALC_BG, fill_opacity=0.95,
                    corner_radius=0.08,
                )
                # Add bg behind (send to back)
                self.play(FadeIn(calc_bg), run_time=0.2)
                self.bring_to_front(eq_line1)

                # Show numeric line
                self.play(Write(eq_line2), run_time=0.8)
                self.wait(0.3)
                # Show activation line
                self.play(Write(act_tex), run_time=0.5)
                self.wait(0.8)

                # ── Place result value on neuron ──
                vl = Text(f"{act_val:.2g}", font_size=16, color=ACCENT)
                vl.next_to(neurons[l_idx][n_idx], UP, buff=0.12)
                value_labels[(l_idx, n_idx)] = vl

                result_col = ACCENT
                result_opacity = 0.5
                if is_relu and z_val <= 0:
                    result_col = RED
                    result_opacity = 0.3

                # ── Clean up: fade calc, show result ──
                self.play(
                    FadeOut(calc_bg), FadeOut(eq_line1),
                    FadeOut(eq_line2), FadeOut(act_tex),
                    FadeIn(vl),
                    neurons[l_idx][n_idx].animate.set_fill(
                        result_col, opacity=result_opacity
                    ).set_stroke(layer_colors[l_idx], width=2.5),
                    run_time=0.5,
                )

                for e in incoming:
                    e.set_stroke(WEIGHT_COL, width=1.2, opacity=0.5)

                # ── Zoom out, restore ──
                self.play(
                    self.camera.frame.animate.set_width(
                        default_frame_width
                    ).move_to(default_frame_center),
                    others.animate.set_opacity(1),
                    run_time=0.6,
                )

            self.wait(0.5)

        # ── Final output ──
        out_cap = make_caption(
            f"Output: y_hat = ({y_hat[0]:.2f}, {y_hat[1]:.2f})"
        )
        self.play(FadeIn(out_cap))
        self.wait(2.5)

        all_vl = VGroup(*value_labels.values())
        self.play(
            FadeOut(all_vl), FadeOut(out_cap),
            FadeOut(all_neuron_mobs), FadeOut(all_edges),
            FadeOut(ll_group), FadeOut(nl_group), FadeOut(net_title),
            FadeOut(wb_group),
            run_time=1,
        )
        self.wait(0.3)

        # ═══════════════════════════════════════════════
        # PART 5 – WHY NONLINEARITIES MATTER
        # ═══════════════════════════════════════════════
        why_title = Text("Why Nonlinearities Matter", font_size=40, color=ACCENT)
        why_title.to_edge(UP, buff=0.5)
        self.play(Write(why_title))

        cap6 = make_caption(
            "Without activations, every layer is just an affine map."
        )
        self.play(FadeIn(cap6))
        self.wait(1.5)

        eq1 = MathTex(
            r"h = W^{(1)} x + b^{(1)}", font_size=34
        ).shift(UP * 1 + LEFT * 2)
        eq2 = MathTex(
            r"\hat{y} = W^{(2)} h + b^{(2)}", font_size=34
        ).next_to(eq1, DOWN, buff=0.4)
        self.play(Write(eq1), Write(eq2))
        self.wait(1.5)

        self.play(FadeOut(cap6))
        cap7 = make_caption(
            "Composing affine maps gives another affine map. Depth adds nothing."
        )
        self.play(FadeIn(cap7))

        eq3 = MathTex(
            r"\hat{y} = W^{(2)}(W^{(1)} x + b^{(1)}) + b^{(2)}",
            font_size=34,
        ).shift(UP * 1 + RIGHT * 2)
        eq4 = MathTex(
            r"= \underbrace{W^{(2)} W^{(1)}}_{A} x"
            r"+ \underbrace{W^{(2)} b^{(1)} + b^{(2)}}_{c}",
            font_size=32,
        ).next_to(eq3, DOWN, buff=0.4)
        self.play(Write(eq3))
        self.wait(1)
        self.play(Write(eq4))
        self.wait(2)

        self.play(FadeOut(cap7))
        cap8a = make_caption(
            "The only patterns you can fit are affine ones: lines, planes, hyperplanes."
        )
        self.play(FadeIn(cap8a))
        self.wait(2.5)

        self.play(FadeOut(cap8a))
        cap8b = make_caption(
            "Nonlinearities let the network bend and curve to fit complex data."
        )
        self.play(FadeIn(cap8b))
        self.wait(2.5)

        self.play(*[FadeOut(m) for m in
                     [why_title, eq1, eq2, eq3, eq4, cap8b]])
        self.wait(0.3)

        # ═══════════════════════════════════════════════
        # PART 6 – PIECEWISE LINEAR RELU
        # ═══════════════════════════════════════════════
        relu_title = Text(
            "ReLU Builds Piecewise\nLinear Functions",
            font_size=38, color=ACCENT,
        )
        relu_title.to_edge(UP, buff=0.4)
        self.play(Write(relu_title))

        cap9 = make_caption("A single ReLU bends a line at one point.")
        self.play(FadeIn(cap9))

        axes_relu = Axes(
            x_range=[-3, 3, 1], y_range=[-0.5, 3, 1],
            x_length=5, y_length=3,
            axis_config={"include_numbers": True, "font_size": 22},
        ).shift(DOWN * 0.5)
        relu_graph = axes_relu.plot(
            lambda x: max(0, x), x_range=[-3, 3, 0.01],
            color=RELU_COL, stroke_width=3,
        )
        relu_label = MathTex(
            r"\sigma(x) = \max\{0, x\}", font_size=30, color=RELU_COL,
        ).next_to(axes_relu, RIGHT, buff=0.3).shift(UP * 0.5)
        self.play(Create(axes_relu), run_time=1)
        self.play(Create(relu_graph), Write(relu_label), run_time=1.5)
        self.wait(2)
        self.play(
            FadeOut(axes_relu), FadeOut(relu_graph),
            FadeOut(relu_label), FadeOut(cap9),
        )

        cap10 = make_caption(
            "Composing two ReLU layers gives three linear pieces."
        )
        self.play(FadeIn(cap10))

        axes_pw = Axes(
            x_range=[-1, 4, 1], y_range=[-0.5, 2, 1],
            x_length=7, y_length=3.5,
            axis_config={"include_numbers": True, "font_size": 22},
        ).shift(DOWN * 0.5)

        def f_pw(x):
            if x <= 1:
                return 1.0
            elif x <= 2:
                return 2 - x
            else:
                return 0.0

        pw_graph = axes_pw.plot(
            f_pw, x_range=[-1, 4, 0.01], color=RELU_COL, stroke_width=3,
        )
        pw_eq = MathTex(
            r"f(x) = \sigma\!\bigl(-\sigma(x-1)+1\bigr)", font_size=30,
        ).next_to(axes_pw, RIGHT, buff=0.2).shift(UP * 0.5)
        self.play(Create(axes_pw), run_time=1)
        self.play(Create(pw_graph), Write(pw_eq), run_time=1.5)
        self.wait(1.5)

        bp1 = Dot(axes_pw.c2p(1, 1), color=ACCENT, radius=0.08)
        bp2 = Dot(axes_pw.c2p(2, 0), color=ACCENT, radius=0.08)
        bp1_lbl = MathTex(r"x=1", font_size=22, color=ACCENT).next_to(
            bp1, UP, buff=0.15
        )
        bp2_lbl = MathTex(r"x=2", font_size=22, color=ACCENT).next_to(
            bp2, UP + RIGHT, buff=0.15
        )

        self.play(FadeOut(cap10))
        cap11 = make_caption(
            "Breakpoints at x=1 and x=2 where slope changes."
        )
        self.play(
            FadeIn(bp1), FadeIn(bp2),
            FadeIn(bp1_lbl), FadeIn(bp2_lbl), FadeIn(cap11),
        )
        self.wait(1.5)

        p1 = MathTex(r"f=1", font_size=24, color=GREEN).move_to(
            axes_pw.c2p(-0.2, 1.3)
        )
        p2 = MathTex(r"f=2-x", font_size=24, color=GREEN).move_to(
            axes_pw.c2p(1.5, 0.9)
        )
        p3 = MathTex(r"f=0", font_size=24, color=GREEN).move_to(
            axes_pw.c2p(3.2, 0.3)
        )
        self.play(FadeIn(p1), FadeIn(p2), FadeIn(p3))
        self.wait(2)

        self.play(*[FadeOut(m) for m in [
            relu_title, axes_pw, pw_graph, pw_eq,
            bp1, bp2, bp1_lbl, bp2_lbl, p1, p2, p3, cap11,
        ]])
        self.wait(0.3)

        # ═══════════════════════════════════════════════
        # PART 7 – PARAMETER COUNTING
        # ═══════════════════════════════════════════════
        pc_title = Text("Counting Parameters", font_size=40, color=ACCENT)
        pc_title.to_edge(UP, buff=0.5)
        self.play(Write(pc_title))

        cap12 = make_caption(
            "A layer with a inputs and b outputs has b times (a+1) parameters."
        )
        self.play(FadeIn(cap12))

        formula = MathTex(
            r"\text{Layer } \mathbb{R}^a \to \mathbb{R}^b:",
            r"\; b \times a \text{ weights}"
            r" + b \text{ biases} = b(a+1)",
            font_size=30,
        ).shift(UP * 0.5)
        self.play(Write(formula), run_time=1.5)
        self.wait(2)

        self.play(FadeOut(cap12))
        cap13 = make_caption(
            "For our 2-3-3-2 network: 9 + 12 + 8 = 29 parameters."
        )
        self.play(FadeIn(cap13))

        count_table = VGroup(
            MathTex(r"2 \to 3: \; 3(2+1) = 9", font_size=30),
            MathTex(r"3 \to 3: \; 3(3+1) = 12", font_size=30),
            MathTex(r"3 \to 2: \; 2(3+1) = 8", font_size=30),
            MathTex(
                r"\text{Total: } 9 + 12 + 8 = 29",
                font_size=32, color=ACCENT,
            ),
        ).arrange(DOWN, buff=0.35).shift(DOWN * 1)
        for row in count_table:
            self.play(Write(row), run_time=0.7)
        self.wait(2.5)

        self.play(*[FadeOut(m) for m in [pc_title, formula, count_table, cap13]])
        self.wait(0.3)

        # ═══════════════════════════════════════════════
        # PART 8 – SUMMARY
        # ═══════════════════════════════════════════════
        summary_title = Text("Summary", font_size=44, color=ACCENT)
        summary_title.to_edge(UP, buff=0.6)
        self.play(Write(summary_title))

        bullets = VGroup(
            Text("1. A NN learns weights to fit data", font_size=26),
            Text("2. Fixed weights = just a function", font_size=26),
            Text("3. Each layer = affine map + activation", font_size=26),
            Text("4. Without nonlinearities, only affine fits", font_size=26),
            Text("5. ReLU creates piecewise linear maps", font_size=26),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.35).shift(DOWN * 0.2)
        for b in bullets:
            self.play(FadeIn(b, shift=RIGHT * 0.3), run_time=0.7)
            self.wait(0.4)

        cap_final = make_caption(
            "Next: training these networks with backpropagation!"
        )
        self.play(FadeIn(cap_final))
        self.wait(3)

        self.play(*[FadeOut(m) for m in self.mobjects], run_time=1.5)
        self.wait(0.5)
