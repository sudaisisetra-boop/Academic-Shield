def grade_physics_item1(rd_input, density_b_input):
    score = 0
    feedback = []
    if 0.89 <= rd_input <= 0.91:
        score += 50
        feedback.append("✅ Q1 Correct!")
    else:
        feedback.append("❌ Q1 Incorrect. Hint: RD_pillar = Fraction_submerged * RD_liquid.")

    if 1220 <= density_b_input <= 1240:
        score += 50
        feedback.append("✅ Q2 Correct!")
    else:
        feedback.append("❌ Q2 Incorrect. Consider the extra 50N weight.")

    return score, "\n".join(feedback)
