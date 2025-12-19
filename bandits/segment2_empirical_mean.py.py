from shared import *

class EmpiricalMean(Scene):
    """
    Segment 2: Empirical mean animation from sampled values.
    """

    def construct(self):
        header = Text("Empirical Mean Calculation from Samples", font_size=34).to_edge(UP)
        self.play(FadeIn(header))

        mu, sigma, n_samples = 0.5, 1.0, 10
        np.random.seed(SEED_MEAN)
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
            self.play(Write(formula_tex))
            self.wait(0.25)

            self.play(FadeOut(formula_tex), FadeOut(dot_bell), FadeOut(sample_text))

            emp_mean = means[i]
            mean_dot = Dot(number_line.n2p(emp_mean), color=RED)
            mean_label = MathTex(r"\hat\mu").next_to(mean_dot, UP)
            n_label = Text(f"n={i+1}", font_size=28).next_to(mean_dot, DOWN)

            self.play(FadeIn(mean_dot), FadeIn(mean_label), FadeIn(n_label), run_time=0.35)
            self.wait(0.4)
            self.play(FadeOut(mean_dot), FadeOut(mean_label), FadeOut(n_label), run_time=0.2)

        self.play(
            FadeOut(number_line), FadeOut(mu_dot), FadeOut(mu_label),
            FadeOut(axes), FadeOut(bell_curve), FadeOut(dist_formula), FadeOut(header)
        )
