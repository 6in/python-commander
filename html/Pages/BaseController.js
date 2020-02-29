/**
 * 共通処理等をここに記述
 */

Ext.define('Pages.BaseController', {
    extend: 'Ext.app.ViewController',
    init() {
        const me = this
        me.callParent(arguments)
    },
    post(url, data = {}, headers = {}) {

    },
    get(url) {
        return new Promise((resolve, reject) => {
            Ext.Ajax.request({
                url: url,
                success(response, opts) {
                    resolve({ response, opts });
                },
                failure(response, opts) {
                    reject({ response, opts })
                }
            })
        });
    }
});
