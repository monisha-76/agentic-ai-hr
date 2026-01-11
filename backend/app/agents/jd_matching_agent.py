# agents/jd_matching_agent.py
class JDMatchingAgent:
    def __init__(self):
        pass

    def match_resume_to_jds(self, resume_skills: list, jds: list, top_k=3):
        """
        Match a resume's skills against all JDs.
        Returns top_k JD matches with score, matched skills, and rank.
        """
        results = []

        for jd in jds:
            jd_skills = jd.get("skills", [])
            matched_skills = list(set(resume_skills) & set(jd_skills))
            score = len(matched_skills) / max(len(jd_skills), 1)

            results.append({
                "jd_id": str(jd["_id"]),
                "title": jd.get("title"),
                "score": round(score, 2),
                "matched_skills": matched_skills
            })

        # Sort by score descending
        results.sort(key=lambda x: x["score"], reverse=True)

        # Assign rank
        for i, result in enumerate(results, start=1):
            result["rank"] = i

        return results[:top_k]