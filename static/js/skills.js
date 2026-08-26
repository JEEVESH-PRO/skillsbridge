/* Skill Gap Modal & Course Sourcing Handler */

function showSourceModal(skillName, coursesJson) {
    const modalTitle = document.getElementById('sourceModalTitle');
    const modalContent = document.getElementById('sourceModalContent');

    if (!modalTitle || !modalContent) return;

    modalTitle.innerHTML = `<span style="color: var(--primary);">Upskill:</span> ${skillName}`;
    
    let courses = [];
    try {
        courses = typeof coursesJson === 'string' ? JSON.parse(coursesJson) : coursesJson;
    } catch (e) {
        console.error("Failed to parse courses", e);
    }

    if (!courses || courses.length === 0) {
        modalContent.innerHTML = `
            <div style="text-align: center; padding: 2rem; color: var(--text-muted);">
                <p>No curated courses found for ${skillName} at this time.</p>
                <a href="/learning" class="btn btn-primary btn-sm" style="margin-top: 1rem;">Explore All Courses</a>
            </div>
        `;
    } else {
        let html = '<div style="display: flex; flex-direction: column; gap: 1rem;">';
        courses.forEach(c => {
            let badgeClass = 'badge-matched';
            let badgeText = c.source_type || 'course';
            if (c.source_type === 'youtube') badgeText = 'YouTube Free';
            else if (c.source_type === 'company') badgeText = 'Employer Partner';
            else if (c.source_type === 'platform') badgeText = 'Platform Course';

            html += `
                <div class="glass-panel" style="padding: 1.25rem; display: flex; flex-direction: column; gap: 0.6rem; border-color: rgba(99, 102, 241, 0.2);">
                    <div style="display: flex; justify-content: space-between; align-items: center;">
                        <span class="badge ${c.source_type === 'company' ? 'badge-domain' : 'badge-matched'}">${badgeText}</span>
                        <span style="font-size: 0.8rem; color: var(--text-muted);">${c.duration || 'Self-Paced'} • ${c.difficulty || 'Intermediate'}</span>
                    </div>
                    <h4 style="font-size: 1.1rem; color: #fff;">${c.title}</h4>
                    <p style="font-size: 0.85rem; color: var(--text-muted);">Provider: ${c.provider}</p>
                    <div style="display: flex; justify-content: flex-end; margin-top: 0.5rem;">
                        <a href="${c.url}" target="_blank" rel="noopener" class="btn btn-primary btn-sm">
                            Start Learning ↗
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
