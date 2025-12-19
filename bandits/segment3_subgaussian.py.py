from shared import *

class SubGaussian(Scene):
    """
    Segment 3: Sub-Gaussian concentration bound + illustrative plots.
    """

    def construct(self):
        header = Text("Sub-Gaussian Concentration Bound", font_size=36).to_edge(UP)
        self.play(FadeIn(header))

        formula = MathTex(
            r"\mathbb{P}\left(\hat\mu \geq \mu+\varepsilon\right) \leq \exp\!\left(-\frac{n\varepsilon^2}{2\sigma^2}\right)"
        ).to_edge(UP, buff=1.5)
        self.play(Write(formula))
        self.wait(0.7)

        sigma = 1.0

        # Plot 1: P vs n (eps fixed)
        axes1 = Axes(
            x_range=[0, 40, 5], y_range=[0, 1, 0.1],
            x_length=6, y_length=3.2, axis_config={"include_tip": False}
        ).shift(LEFT * 3 + DOWN * 0.5)

        eps = 0.5
        graph1 = axes1.plot(lambda n: np.exp(-n * eps**2 / (2 * sigma**2)), x_range=[0, 40], color=BLUE)
        label1 = MathTex(r"\varepsilon=0.5,\ \sigma=1").next_to(axes1, UP)
        axes1_labels = axes1.get_axis_labels(MathTex("n"))

        self.play(Create(axes1), Write(axes1_labels), FadeIn(label1))
        self.play(Create(graph1), run_time=1.8)
        self.wait(0.6)
        self.play(FadeOut(VGroup(axes1, axes1_labels, label1, graph1)))

        # Plot 2: P vs eps (n fixed)
        axes2 = Axes(
            x_range=[0, 2, 0.2], y_range=[0, 1, 0.1],
            x_length=6, y_length=3.2, axis_config={"include_tip": False}
        ).shift(RIGHT * 3 + DOWN * 0.5)

        n_fixed = 20
        graph2 = axes2.plot(lambda e: np.exp(-n_fixed * e**2 / (2 * sigma**2)), x_range=[0, 2], color=GREEN)
        label2 = MathTex(r"n=20,\ \sigma=1").next_to(axes2, UP)
        axes2_labels = axes2.get_axis_labels(MathTex(r"\varepsilon"))

        self.play(Create(axes2), Write(axes2_labels), FadeIn(label2))
        self.play(Create(graph2), run_time=1.8)
        self.wait(0.8)

        self.play(FadeOut(VGroup(axes2, axes2_labels, label2, graph2, formula, header)))
