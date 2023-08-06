import { ICellComment, ICellSelectionComment } from './commentformat';
import { CommentFileModel, CommentWidgetFactory } from '../api';
import { Cell } from '@jupyterlab/cells';
import { INotebookTracker } from '@jupyterlab/notebook';
import { CellCommentWidget, CellSelectionCommentWidget } from './widget';
import { docFromCell, markCommentSelection } from './utils';

export class CellCommentWidgetFactory<
  C extends ICellComment = ICellComment
> extends CommentWidgetFactory<Cell, C> {
  constructor(options: CellCommentWidgetFactory.IOptions) {
    super(options);

    this._tracker = options.tracker;
  }

  createWidget(
    comment: ICellComment,
    model: CommentFileModel,
    target?: Cell
  ): CellCommentWidget | undefined {
    const cell = target ?? this._cellFromID(comment.target.cellID);
    if (cell == null) {
      console.error('Cell not found for comment', comment);
      return;
    }

    return new CellCommentWidget({
      model,
      comment,
      target: cell
    });
  }

  private _cellFromID(id: string): Cell | undefined {
    const notebook = this._tracker.currentWidget;
    if (notebook == null) {
      return;
    }

    return notebook.content.widgets.find(cell => cell.model.id === id);
  }

  readonly widgetType = 'cell';
  readonly commentType = 'cell';

  private _tracker: INotebookTracker;
}

export namespace CellCommentWidgetFactory {
  export interface IOptions extends CommentWidgetFactory.IOptions {
    tracker: INotebookTracker;
  }
}

export class CellSelectionCommentWidgetFactory extends CommentWidgetFactory<
  Cell,
  ICellSelectionComment
> {
  constructor(options: CellCommentWidgetFactory.IOptions) {
    super(options);

    this._tracker = options.tracker;
  }

  createWidget(
    comment: ICellSelectionComment,
    model: CommentFileModel,
    target?: Cell
  ): CellSelectionCommentWidget | undefined {
    const cell = target ?? this._cellFromID(comment.target.cellID);
    if (cell == null) {
      console.error('Cell not found for comment', comment);
      return;
    }

    const mark = markCommentSelection(docFromCell(cell), comment);

    return new CellSelectionCommentWidget({
      model,
      comment,
      mark,
      target: cell
    });
  }

  private _cellFromID(id: string): Cell | undefined {
    const notebook = this._tracker.currentWidget;
    if (notebook == null) {
      return;
    }

    return notebook.content.widgets.find(cell => cell.model.id === id);
  }

  readonly widgetType = 'cell-selection';
  readonly commentType = 'cell-selection';

  private _tracker: INotebookTracker;
}
