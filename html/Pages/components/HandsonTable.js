Ext.define('Pages.components.HandsonTable', {
    extend: 'Ext.Component',
    alias: 'widget.handson-table',
    config: {
        data: [],
        rowHeaders: true,
        colHeaders: true,
        contextMenu: true,
        manualColumnResize: true,
        manualRowResize: true,
        currentRowClassName: 'currentRow',
        currentColClassName: 'currentCol',
        manualColumnMove: true,
        manualRowMove: true,
        customBorders: true,
        mergeCells: true,
        outsideClickDeselects: false,
        search: true
    },
    twoWayBindable: [
        'data'
    ],
    constructor(config) {
        this.callParent([config])
        return
    },
    initComponent() {
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
            const elm = document.getElementById(id);
            const options = Object.assign(
                {
                    rowHeaders: me.getRowHeaders(),
                    colHeaders: me.getColHeaders(),
                    contextMenu: me.getContextMenu(),
                    manualColumnResize: me.getManualColumnResize(),
                    manualRowResize: me.getManualRowResize(),
                    currentRowClassName: me.getCurrentRowClassName(),
                    currentColClassName: me.getCurrentColClassName(),
                    manualColumnMove: me.getManualColumnMove(),
                    manualRowMove: me.getManualRowMove(),
                    customBorders: me.getCustomBorders(),
                    mergeCells: me.getMergeCells(),
                    outsideClickDeselects: me.getOutsideClickDeselects(),
                    search: me.getSearch(),
                    data: me.config.data
                }
            );

            me.grid = new Handsontable(elm, options);
        },
        resize(obj, width, height) {
            const me = this;
            if (me.grid) {
                me.grid.updateSettings({ width, height });
            }
        }
    },
    applyData(value) {
        const me = this
        if (me.grid) {
            me.grid.loadData(value);
            me.grid.render();
        }
    },
    getData() {
        const me = this;
        me.callParent(arguments);
        if (me.grid) {
            return me.grid.getData();
        }
    }

});
