/** @jsx jsx */
import { jsx, css } from '@emotion/react';
// import { VegaLite } from 'react-vega';
import { useModelState, GraphSpec, EncodingInfo } from '../hooks/bifrost-model';
import {
  deleteSpecFilter,
  updateSpecFilter,
  addDefaultFilter,
} from '../modules/VegaFilters';
import React, { useEffect, useState } from 'react';
import BifrostVega from '../modules/BifrostVega';
import { View } from 'vega';
import theme from '../theme';
import { VegaEncoding } from '../modules/VegaEncodings';
import RangeSlider from './ui-widgets/RangeSlider';
import useSpecHistory from '../hooks/useSpecHistory';

const graphCss = css`
  padding-left: 34px;
  overflow-x: auto;

  g.mark-text.role-axis-title {
    text.hovered {
      fill: ${theme.color.primary.dark};
    }
  }
`;

const axisCss = css`
  cursor: pointer;
`;

interface GraphProps {
  sideBarRef: React.RefObject<HTMLDivElement>;
  graphRef: React.RefObject<HTMLDivElement>;
  clickedAxis: VegaEncoding | '';
  updateClickedAxis: (encoding: VegaEncoding | '') => void;
  sideBarOpen: boolean;
  clickSidebarButton: () => void;
  onViewCreated(vegaView: View): void;
  selection: string;
}

export type GraphSpecProps = keyof GraphSpec;

export default function Graph(props: GraphProps) {
  const [selectedData, setSelectedData] = useModelState('selected_data');
  const [spec, setSpec] = useModelState('graph_spec');
  const [graphBounds, setGraphBounds] = useModelState('graph_bounds');
  const [axisState, setAxisState] = useState<Record<string, string>>({
    activeAxis: props.clickedAxis,
  });
  const data = useModelState('graph_data')[0];

  useEffect(() => {
    if (['x', 'y'].includes(props.clickedAxis)) {
      setAxisState({ activeAxis: props.clickedAxis });
    } else {
      setAxisState({ activeAxis: '' });
    }
  }, [props.clickedAxis]);

  const graphData = { data };

  // multiple signals can be added by adding a new field
  const signalListeners = { brush: handleBrush };

  function handleBrush(...args: any) {
    setSelectedData(args);
  }

  function getBoundingBox(el: Element) {
    const xBoundingBox = el.getBoundingClientRect();
    return {
      top: xBoundingBox.top,
      right: xBoundingBox.right,
      bottom: xBoundingBox.bottom,
      left: xBoundingBox.left,
    };
  }

  function getAxisBoundingBoxes(
    wrapper: HTMLDivElement
  ): Record<string, Record<string, number>> {
    const xAxisLabel = wrapper.querySelector(
      "g[aria-label^='X-axis'] .mark-text.role-axis-title"
    );
    const yAxisLabel = wrapper.querySelector(
      "g[aria-label^='Y-axis'] .mark-text.role-axis-title"
    );

    const boundingBoxes: Record<string, Record<string, any>> = {};

    if (xAxisLabel) {
      boundingBoxes['x'] = getBoundingBox(xAxisLabel);
    }
    if (yAxisLabel) {
      boundingBoxes['y'] = getBoundingBox(yAxisLabel);
    }

    return boundingBoxes;
  }

  function updateGraphBounds() {
    const brushIsActive =
      selectedData[1] && Object.keys(selectedData[1]).length;
    if (!brushIsActive) {
      return;
    }
    const graphBounds = selectedData[1];

    // Assign the ranges to the spec
    const fields = Object.keys(graphBounds);
    const snapshotSpec = fields.reduce((newSpec, field) => {
      const fieldInfo = Object.values(spec.encoding).find(
        (info) => info.field === field
      );
      const type = fieldInfo.type as string;
      if (!fieldInfo) {
        return newSpec;
      }
      return updateSpecFilter(
        newSpec,
        field,
        type === 'quantitative' ? 'range' : 'oneOf',
        graphBounds[field],
        { compoundOperator: 'and' }
      );
    }, spec);
    setSpec(snapshotSpec);
    setGraphBounds(graphBounds);
  }

  function resetBrushView() {
    const fields = Object.keys(graphBounds);

    const snapshotSpec = fields.reduce((newSpec, field) => {
      const fieldInfo = Object.values(spec.encoding).find(
        (info) => info.field === field
      );
      const type = fieldInfo.type as EncodingInfo['type'];
      if (!fieldInfo) {
        return newSpec;
      }
      const temp = deleteSpecFilter(
        newSpec,
        field,
        type === 'quantitative' ? 'range' : 'oneOf',
        { compoundOperator: 'and' }
      );
      return addDefaultFilter(temp, data, type, field);
    }, spec);
    setSpec(snapshotSpec);

    setGraphBounds({});
  }

  function handleClickOnAxis(channel: VegaEncoding) {
    if (!props.sideBarOpen) {
      props.clickSidebarButton();
      return;
    }
    const field = spec.encoding[channel].field;

    const pillList =
      props.sideBarRef.current?.getElementsByClassName('pill-list')[0];

    let newChannel: VegaEncoding | '' =
      axisState['activeAxis'] === channel ? '' : channel;

    if (!pillList) {
      newChannel = '';
    } else {
      const pills = pillList.getElementsByClassName('graph-pill');
      if (pills) {
        Array.from(pills).forEach((pill) => {
          if (
            pill.querySelectorAll('.pill-header span')[1].textContent === field
          ) {
            (
              pill.querySelectorAll('.pill-header span')[1] as HTMLElement
            ).click();
          }
        });
      }
    }
    props.updateClickedAxis(newChannel);
  }

  function placeAxisWrappers() {
    if (!props.graphRef.current) {
      return;
    }
    const wrapper = props.graphRef.current;
    const parentBoundingBox = wrapper.getBoundingClientRect();
    const axisBoundingBoxes = getAxisBoundingBoxes(wrapper);

    const xAxisBoundingBox = axisBoundingBoxes['x'];
    const yAxisBoundingBox = axisBoundingBoxes['y'];

    const xAxisWrapper = wrapper.getElementsByClassName(
      'x-axis-wrapper'
    )[0] as HTMLElement;

    const yAxisWrapper = wrapper.getElementsByClassName(
      'y-axis-wrapper'
    )[0] as HTMLElement;

    if (xAxisBoundingBox) {
      xAxisWrapper.setAttribute(
        'style',
        `width:${xAxisBoundingBox.right - xAxisBoundingBox.left}px; height: ${
          xAxisBoundingBox.bottom - xAxisBoundingBox.top
        }px;
        position: absolute;
        left: ${xAxisBoundingBox.left - parentBoundingBox.left}px;
        top: ${xAxisBoundingBox.top - parentBoundingBox.top + 40}px;
        `
      );
    }

    if (yAxisBoundingBox) {
      yAxisWrapper.setAttribute(
        'style',
        `width:${yAxisBoundingBox.right - yAxisBoundingBox.left}px; height: ${
          yAxisBoundingBox.bottom - yAxisBoundingBox.top
        }px;
        position: absolute;
        left: ${yAxisBoundingBox.left - parentBoundingBox.left}px;
        top: ${yAxisBoundingBox.top - parentBoundingBox.top + 40}px;`
      );
    }
  }

  function onNewView(view: View) {
    setTimeout(() => placeAxisWrappers(), 100);
    props.onViewCreated(view);
  }

  function handleMouseEnter(channel: VegaEncoding) {
    if (!props.graphRef) {
      return;
    }
    const wrapper = props.graphRef.current;
    if (channel === 'x') {
      const xAxis = wrapper?.querySelector(
        "g[aria-label^='X-axis'] .mark-text.role-axis-title text"
      );
      xAxis?.classList.add('hovered');
    } else {
      const yAxis = wrapper?.querySelector(
        "g[aria-label^='Y-axis'] .mark-text.role-axis-title text"
      );
      yAxis?.classList.add('hovered');
    }
  }

  function handleMouseLeave(channel: VegaEncoding) {
    if (!props.graphRef) {
      return;
    }
    const wrapper = props.graphRef.current;
    if (channel === 'x') {
      const xAxis = wrapper?.querySelector(
        "g[aria-label^='X-axis'] .mark-text.role-axis-title text"
      );
      xAxis?.classList.remove('hovered');
    } else {
      const yAxis = wrapper?.querySelector(
        "g[aria-label^='Y-axis'] .mark-text.role-axis-title text"
      );
      yAxis?.classList.remove('hovered');
    }
  }

  return (
    <div css={graphCss} onDoubleClick={resetBrushView}>
      <div
        // style={{ width: '100%', height: '100%' }}
        onMouseUp={updateGraphBounds}
        onMouseLeave={() => setSelectedData(['brush', {}])}
      >
        <BifrostVega
          spec={spec}
          data={graphData}
          signalListeners={
            props.selection === 'brush' ? signalListeners : undefined
          }
          renderer={'svg'}
          actions={false}
          onNewView={onNewView}
        />
      </div>
      <div
        className="x-axis-wrapper"
        onClick={() => handleClickOnAxis('x')}
        onMouseEnter={() => handleMouseEnter('x')}
        onMouseLeave={() => handleMouseLeave('x')}
        css={axisCss}
      ></div>
      <div
        className="y-axis-wrapper"
        onClick={() => handleClickOnAxis('y')}
        onMouseEnter={() => handleMouseEnter('y')}
        onMouseLeave={() => handleMouseLeave('y')}
        css={axisCss}
      ></div>
      {axisState['activeAxis'] !== '' &&
        axisState['activeAxis'] in spec.encoding &&
        !['nominal', 'oridnal'].includes(
          spec.encoding[axisState['activeAxis'] as VegaEncoding].type
        ) && (
          <AxisRangeSlider
            graphSpec={spec}
            setGraphSpec={setSpec}
            field={spec.encoding[axisState['activeAxis'] as VegaEncoding].field}
            axis={axisState['activeAxis']}
          />
        )}
    </div>
  );
}

function AxisRangeSlider({
  graphSpec,
  setGraphSpec,
  field,
  axis,
}: {
  graphSpec: GraphSpec;
  setGraphSpec: (val: GraphSpec, options?: any) => void;
  field: string;
  axis: string;
}) {
  const [columnRanges] = useModelState('df_column_ranges');
  const bounds = columnRanges[field];
  const range = getRange();
  const save = useSpecHistory();

  // Initialize a slider if one doesn't exist
  useEffect(() => {
    if (!range) {
      updateRange(bounds);
    }
  }, []);

  function getRange(): [number, number] | undefined {
    const type = 'range';
    const foundTransform = graphSpec.transform.find(
      (f) =>
        'or' in f.filter &&
        f.filter.or[0]?.field === field &&
        type in f.filter.or[0]
    );
    return foundTransform?.filter.or?.[0][type];
  }

  function updateRange(range: readonly number[]) {
    let newRange = range.slice();
    if (range[0] > range[1]) {
      newRange = [range[1], range[0]];
    }
    const newSpec = updateSpecFilter(graphSpec, field, 'range', newRange);

    setGraphSpec(newSpec);
  }

  const axisStyles: React.CSSProperties | undefined =
    axis === 'y'
      ? {
          position: 'absolute',
          bottom: '-20px',
          left: '-450px',
          transformOrigin: 'right center',
          transform: 'rotate(90deg)',
        }
      : undefined;

  const width = axis === 'y' ? 470 : 640;

  return (
    <div style={axisStyles}>
      <RangeSlider
        width={width}
        domain={bounds}
        values={range}
        onUpdate={(update) => updateRange(update)}
        onSlideEnd={() =>
          save(graphSpec, `Updated the filter range for ${field}`)
        }
        vertical={axis === 'y'}
        reversed={axis === 'y'}
        onAxis={true}
      />
    </div>
  );
}
