Ext.define('Pages.components.Iframe', {
    extend: 'Ext.Component',
    alias: 'widget.iframe',
    config: {
        src: '',
        target: ''
    },
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
    renderTpl: '<iframe id="{id}_component" src="{src}" target="{target}" width="100%" height="100%"></iframe>',

    listeners: {
        /**
         * コンポーネント本体描画後に呼び出れる。
         * 外部のコンポーネントを初期化するタイミングはこちらで。
         */
        afterrender() {
            const me = this;
            // 表示領域を取得する
            const id = `${this.getId()}_component`;
            const elm = document.getElementById(id);
            me.iframe = elm;
            // me.iframe.src = me.config.src;
        }
    },

    applySrc(value) {
        const me = this;
        if (me.iframe) {
            me.iframe.src = value;
        }
    },
    // applyTarget(value) {
    //     const me = this;
    //     if (me.iframe) {
    //         me.iframe.target = value;
    //     }
    // }

});
