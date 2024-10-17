        // Copyright (c) 2024, Kreatech Group and contributors
// For license information, please see license.txt

const color_percent = [
    {threshold: 40, color: 'red'},
    {threshold: 75, color: 'yellow'},
    {threshold: 100, color: '#90EE90'},
    {threshold: Infinity, color: 'cyan'}
];

const get_color_background = (published_content_percent) => {
    for (const range of color_percent) {
        if (published_content_percent <= range.threshold) {
            return range.color
        }
    }

    return 'transparent'
}

const get_count_of_content_published = (frm, row) => {
    return new Promise((resolve, reject) => {
        frappe.call({
            method: "app_marketing.app_marketing.doctype.planificador_contenido.planificador_contenido.get_all_content_for_brand_and_type",
            args: {
                period: frm.doc.name,
                brand: row.brand,
                social_media: row.social_media,
                type_of_content: row.type_of_content,
            },
            callback: (res) => {
		console.log(res)
                let percent = (res.message[0].count_of_content / row.amount_of_content) * 100;
                if (
                    frm.doc.docstatus === 0 && frm.doc.__islocal !== 1
                )
                    row.published_content = percent;

                resolve(percent);
            },
            error: (err) => {
                reject(err);
            }
        });
    });
}

frappe.ui.form.on('Planificador Contenido', {
    refresh: async (frm) => {
        try {
            for (let i = 0; i < frm.doc.content_planner.length; i++) {
                const d = frm.doc.content_planner[i];
                let percent = await get_count_of_content_published(frm, d);
                let rowElement = $(`div[data-fieldname="content_planner"] .grid-body .rows [data-idx="${d.idx}"]`);
                rowElement.css({
                        'background-color': get_color_background(percent)
                    }
                );
            }
            frm.refresh_field('content_planner')
        } catch (err) {
            console.error('Error en la actualización de contenido:', err);
        }
    }
});

