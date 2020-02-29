Ext.define('Pages.components.TemplateComponent', {
    extend: 'Ext.Component',
    alias: 'widget.template-component',
    config: {
        value: 'value'
    },
    twoWayBindable: [
        'value'
    ],
    constructor(config) {
        this.callParent([config])
        return
    },
    initComponent() {
    },
    setValue(newValue) {
        this.callParent([newValue])
    },
    getValue() {
        return this.callParent(arguments)
    },
    // コンポーネントの表示領域
    renderTpl: '<div id="{id}_component" style="width: 100%; height: 100%">This is a template component.</div>',

    listeners: {
        /**
         * コンポーネント本体描画後に呼び出れる。
         * 外部のコンポーネントを初期化するタイミングはこちらで。
         */
        afterrender() {
            const me = this;
            // 表示領域を取得する
            const id = `${this.getId()}_component`;
            me.elm = document.getElementById(id);
        }
    },
    applyValue(value) {
        const me = this
        if (me.elm) {
        }
    }
});
