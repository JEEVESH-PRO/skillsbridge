/* Skill Gap Modal & Course Sourcing Handler — Editorial Style */

function showSourceModal(skillName, coursesJson) {
    const modalTitle = document.getElementById('sourceModalTitle');
    const modalContent = document.getElementById('sourceModalContent');

    if (!modalTitle || !modalContent) return;

    modalTitle.innerHTML = `${skillName}`;
    
    let courses = [];
    try {
        courses = typeof coursesJson === 'string' ? JSON.parse(coursesJson) : coursesJson;
    } catch (e) {
        console.error("Failed to parse courses", e);
    }

    if (!courses || courses.length === 0) {
        modalContent.innerHTML = `
            <div style="text-align: center; padding: 2rem; color: var(--text-muted);">
                <p style="font-size: 0.9rem;">No curated curriculum modules indexed for ${skillName} at this time.</p>
                <a href="/learning" class="btn btn-secondary btn-sm" style="margin-top: 1rem;">View All Coursework</a>
            </div>
        `;
    } else {
        let html = '<div style="display: flex; flex-direction: column; gap: 0.85rem;">';
        courses.forEach(c => {
            let badgeClass = 'badge-domain';
            let badgeText = c.source_type ? c.source_type.toUpperCase() : 'COURSE';
            if (c.source_type === 'youtube') badgeText = 'VIDEO SPEC';
            else if (c.source_type === 'company') badgeText = 'OFFICIAL PARTNER';
            else if (c.source_type === 'platform') badgeText = 'PLATFORM CURRICULUM';

            html += `
                <div class="editorial-panel" style="padding: 1.25rem; display: flex; flex-direction: column; gap: 0.5rem; background: var(--bg-subtle);">
                    <div style="display: flex; justify-content: space-between; align-items: baseline;">
                        <span class="badge ${badgeClass}" style="font-size: 0.65rem;">${badgeText}</span>
                        <span class="mono-meta" style="font-size: 0.68rem; color: var(--text-dim);">${c.duration || 'SELF-PACED'} • ${c.difficulty ? c.difficulty.toUpperCase() : 'PRODUCTION'}</span>
                    </div>
                    <h4 style="font-size: 1rem; color: var(--text-main); margin-top: 0.2rem;">${c.title}</h4>
                    <span class="mono-meta" style="font-size: 0.7rem; color: var(--text-muted);">PROVIDER // ${c.provider}</span>
                    <div style="display: flex; justify-content: flex-end; margin-top: 0.4rem; border-top: 1px solid var(--border); padding-top: 0.6rem;">
                        <a href="${c.url}" target="_blank" rel="noopener" class="btn btn-primary btn-sm" style="font-size: 0.75rem;">
                            Open Syllabus ↗
                        </a>
                    </div>
                </div>
            `;
        });
        html += '</div>';
        modalContent.innerHTML = html;
    }

    window.openModal('sourceModal');
}

function sourceSkillCourses(skillId, skillName) {
    fetch(`/api/skills/${skillId}/courses`)
        .then(response => {
            if (!response.ok) throw new Error('Network response was not ok');
            return response.json();
        })
        .then(data => {
            showSourceModal(skillName, data.courses || []);
        })
        .catch(err => {
            console.error('Error fetching courses:', err);
            showSourceModal(skillName, []);
        });
}
