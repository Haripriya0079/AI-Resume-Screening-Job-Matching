
const resumeFile = document.getElementById("resumeFile");
const fileName = document.getElementById("fileName");
const analyzeBtn = document.getElementById("analyzeBtn");
const jobDescription = document.getElementById("jobDescription");
const loading = document.getElementById("loading");
const result = document.getElementById("result");

resumeFile.addEventListener("change", function () {
    const file = resumeFile.files[0];

    if (!file) {
        fileName.textContent = "No file selected";
        return;
    }

    const allowedTypes = [".pdf", ".docx"];
    const extension = file.name.toLowerCase().slice(file.name.lastIndexOf("."));

    if (!allowedTypes.includes(extension)) {
        alert("Please upload only PDF or DOCX files.");
        resumeFile.value = "";
        fileName.textContent = "No file selected";
        return;
    }

    fileName.textContent = "Selected: " + file.name;
});

analyzeBtn.addEventListener("click", async function () {
    const file = resumeFile.files[0];
    const jd = jobDescription.value.trim();

    if (!file) {
        alert("Please upload your resume first.");
        return;
    }

    if (!jd) {
        alert("Please enter a job description.");
        return;
    }

    const formData = new FormData();
    formData.append("resume", file);
    formData.append("job_description", jd);

    result.classList.add("hidden");
    loading.classList.remove("hidden");
    analyzeBtn.disabled = true;
    analyzeBtn.textContent = "Analyzing...";

    try {
        const response = await fetch("/analyze", {
            method: "POST",
            body: formData
        });

        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.error || "Analysis failed");
        }

        document.getElementById("score").textContent = data.match_score + "%";

        const matchedList = document.getElementById("matchedSkills");
        const missingList = document.getElementById("missingSkills");
        const suggestionsList = document.getElementById("suggestions");

        matchedList.innerHTML = "";
        missingList.innerHTML = "";
        suggestionsList.innerHTML = "";

        data.matched_skills.forEach(skill => {
            const li = document.createElement("li");
            li.textContent = skill;
            matchedList.appendChild(li);
        });

        data.missing_skills.forEach(skill => {
            const li = document.createElement("li");
            li.textContent = skill;
            missingList.appendChild(li);
        });

        data.suggestions.forEach(suggestion => {
            const li = document.createElement("li");
            li.textContent = suggestion;
            suggestionsList.appendChild(li);
        });

        result.classList.remove("hidden");
        result.scrollIntoView({ behavior: "smooth" });

    } catch (error) {
        alert(error.message || "Something went wrong. Please try again.");
    } finally {
        loading.classList.add("hidden");
        analyzeBtn.disabled = false;
        analyzeBtn.textContent = "Analyze Resume ✨";
    }
});
