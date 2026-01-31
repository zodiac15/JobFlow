export function calculateMatchScore(job, userSkills) {
    if (!userSkills || userSkills.length === 0) return 0;
    if (!job) return 0;

    const text = (job.title + ' ' + (job.description || '')).toLowerCase();
    let matches = 0;

    userSkills.forEach(skill => {
        if (text.includes(skill.toLowerCase())) {
            matches++;
        }
    });

    return Math.round((matches / userSkills.length) * 100);
}
