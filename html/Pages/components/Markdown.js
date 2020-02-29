Ext.define('Pages.components.Markdown', {
    extend: 'Ext.Component',
    alias: 'widget.markdown',
    config: {
        value: ''
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
    renderTpl: '<div id="{id}_component" style="width: 100%; height: 100%"></div>',

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
            me.elm.innerHTML = marked(me.config.value);
        }
    },
    applyValue(value) {
        const me = this
        if (me.elm) {
            me.elm.innerHTML = marked(value);
        }
    }
});
