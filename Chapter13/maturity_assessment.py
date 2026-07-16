"""
Chapter 13 - Implementing an API Security Strategy.
A lightweight self-assessment against the 42Crunch maturity model dimensions
covered in the chapter. Score each 0-3; the tool reports gaps and a roadmap hint.
"""
from dataclasses import dataclass

DIMENSIONS = ["Inventory", "Design", "Development",
              "Testing", "Protection", "Governance"]


@dataclass
class Assessment:
    scores: dict  # dimension -> 0..3

    def gaps(self) -> list[str]:
        return [d for d, s in self.scores.items() if s < 2]

    def overall(self) -> float:
        return round(sum(self.scores.values()) / (3 * len(self.scores)) * 100, 1)

    def report(self) -> str:
        lines = [f"Overall maturity: {self.overall()}%"]
        for d in DIMENSIONS:
            lines.append(f"  {d:<12} {'#' * self.scores.get(d, 0):<3} ({self.scores.get(d,0)}/3)")
        gaps = self.gaps()
        lines.append("Priority focus: " + (", ".join(gaps) if gaps else "none -- sustain"))
        return "\n".join(lines)


if __name__ == "__main__":
    example = Assessment({"Inventory": 1, "Design": 2, "Development": 2,
                          "Testing": 1, "Protection": 3, "Governance": 1})
    print(example.report())
