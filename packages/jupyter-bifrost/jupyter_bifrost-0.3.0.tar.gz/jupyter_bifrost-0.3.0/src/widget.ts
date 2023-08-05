// Copyright (c) waidhoferj
// Distributed under the terms of the Modified BSD License.

import {
  DOMWidgetModel,
  DOMWidgetView,
  ISerializers,
} from '@jupyter-widgets/base';
import React from 'react';
import ReactDOM from 'react-dom';
import BifrostReactWidget from './components/BifrostReactWidget';
import {
  GraphSpec,
  GraphData,
  SuggestedGraphs,
  QuerySpec,
  Args,
  EncodingInfo,
  SelectionData,
  GraphDataConfig,
} from './hooks/bifrost-model';

import { MODULE_NAME, MODULE_VERSION } from './version';

// Import the CSS
import '../css/widget.css';
import { VegaMark } from './modules/VegaEncodings';

const bifrostModelPropDefaults = {
  spec_history: [] as GraphSpec[],
  output_variable: '',
  df_variable_name: '',
  current_dataframe_index: 0,
  graph_spec: {} as GraphSpec,
  query_spec: {} as QuerySpec,
  df_columns: [] as string[],
  df_column_ranges: {} as { [field: string]: [number, number] },
  selected_data: ['', {}] as SelectionData,
  selected_columns: [] as string[],
  passed_kind: '' as VegaMark | '',
  graph_data: {} as GraphData,
  graph_bounds: {} as SelectionData[1],
  suggested_graphs: [] as SuggestedGraphs,
  flags: {},
  passed_encodings: {} as Args,
  column_types: {} as Record<EncodingInfo['field'], EncodingInfo['type']>,
  column_name_map: {} as Record<string, string>,
  graph_data_config: { sampleSize: 100, datasetLength: 1 } as GraphDataConfig,
  df_code: '$df',
  input_url: '',
};

export type ModelState = typeof bifrostModelPropDefaults;

export class BifrostModel extends DOMWidgetModel {
  defaults() {
    return {
      ...super.defaults(),
      _model_name: BifrostModel.model_name,
      _model_module: BifrostModel.model_module,
      _model_module_version: BifrostModel.model_module_version,
      _view_name: BifrostModel.view_name,
      _view_module: BifrostModel.view_module,
      _view_module_version: BifrostModel.view_module_version,
      ...bifrostModelPropDefaults,
    };
  }

  static serializers: ISerializers = {
    ...DOMWidgetModel.serializers,
    // Add any extra serializers here
  };

  static model_name = 'BifrostModel';
  static model_module = MODULE_NAME;
  static model_module_version = MODULE_VERSION;
  static view_name = 'BifrostView'; // Set to null if no view
  static view_module = MODULE_NAME; // Set to null if no view
  static view_module_version = MODULE_VERSION;
}

export class BifrostView extends DOMWidgetView {
  render() {
    this.el.classList.add('bifrost-widget');

    const component = React.createElement(BifrostReactWidget, {
      model: this.model,
    });
    ReactDOM.render(component, this.el);
  }
}
