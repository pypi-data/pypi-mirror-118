/**@jsx jsx */
import { jsx, css } from '@emotion/react';
import {
  Slider,
  Rail,
  Handles,
  Tracks,
  SliderItem,
  GetEventData,
} from 'react-compound-slider';
import { GetRailProps } from 'react-compound-slider/dist/types/Rail/types';
import { GetHandleProps } from 'react-compound-slider/dist/types/Handles/types';
import { GetTrackProps } from 'react-compound-slider/dist/types/Tracks/types';
import { BifrostTheme } from '../../theme';
import React, { Fragment, useCallback, useEffect, useState } from 'react';
import { round } from '../../modules/utils';

const sliderStyle = {
  position: 'relative',
  width: '100%',
};

interface RangeUpdater {
  (values: readonly number[]): void;
}

interface RangeSliderProps {
  domain?: [number, number];
  values?: [number, number];
  width?: number;
  onUpdate: RangeUpdater;
  onSlideEnd?: () => void;
  vertical?: boolean;
  reversed?: boolean;
  onAxis?: boolean;
}

export default function RangeSlider({
  domain = [0, 100],
  values = [0, 20],
  width,
  onUpdate,
  onSlideEnd,
  vertical,
  reversed,
  onAxis,
}: RangeSliderProps) {
  return (
    <div
      className={`RangeSlider${onAxis ? ' onAxis' : ''}`}
      css={css`
        width: 100%;
        padding: 12px;
        width: ${width}px;

        &.onAxis {
          input::-webkit-outer-spin-button,
          input::-webkit-inner-spin-button {
            -webkit-appearance: none;
            margin: 0;
          }
        }
      `}
    >
      <RangeInputs
        values={reversed ? [values[1], values[0]] : values}
        onUpdate={onUpdate}
        reversed={reversed}
      >
        <Slider
          vertical={vertical}
          reversed={reversed}
          className="range-slider"
          mode={1}
          domain={domain}
          rootStyle={sliderStyle}
          onUpdate={onUpdate}
          onSlideEnd={onSlideEnd}
          values={reversed ? [values[1], values[0]] : values}
        >
          <Rail>{(props) => <SliderRail {...props} />}</Rail>
          <Handles>
            {({ handles, getHandleProps }) => (
              <div className="slider-handles">
                {handles.map((handle) => (
                  <Handle
                    key={handle.id}
                    handle={handle}
                    domain={domain}
                    getHandleProps={getHandleProps}
                  />
                ))}
              </div>
            )}
          </Handles>
          <Tracks left={false} right={false}>
            {({ tracks, getTrackProps }) => (
              <div className="slider-tracks">
                {tracks.map(({ id, source, target }) => (
                  <Track
                    key={id}
                    source={source}
                    target={target}
                    getTrackProps={getTrackProps}
                  />
                ))}
              </div>
            )}
          </Tracks>
        </Slider>
      </RangeInputs>
    </div>
  );
}

// *******************************************************
// Range Inputs
// *******************************************************

const rangeInputsCss = css`
  display: flex;
  width: 100%;
  align-items: center;

  input {
    background-color: transparent;
    border: none;
    width: 5em;
    &.start {
      margin-right: 5px;
    }

    &.end {
      margin-left: 15px;
    }
  }

  .content {
    width: 100%;
  }
`;
interface RangeInputsProps {
  children: React.ReactNode;
  values: [number, number];
  onUpdate: RangeUpdater;
  reversed?: boolean;
}

function RangeInputs(props: RangeInputsProps) {
  const [minInput, setMinInput] = useState(props.values[0]);
  const [maxInput, setMaxInput] = useState(props.values[1]);

  useEffect(() => {
    setMinInput(props.values[0]);
    setMaxInput(props.values[1]);
  }, props.values);

  function onSubmit() {
    let min = minInput;
    let max = maxInput;
    if (minInput > maxInput) {
      max = minInput;
      min = maxInput;
      setMinInput(min);
      setMaxInput(max);
    }
    props.onUpdate([min, max]);
  }

  function handleEnter(e: React.KeyboardEvent<HTMLInputElement>) {
    if (e.key !== 'Enter') {
      return;
    }
    const el = e.target as HTMLInputElement;
    el.blur();
  }

  return (
    <div className="RangeInputs" css={rangeInputsCss}>
      <input
        className="start"
        value={round(minInput, 2)}
        type="number"
        name="min"
        onChange={(e) => setMinInput(e.target.valueAsNumber)}
        onBlur={onSubmit}
        onKeyPress={handleEnter}
      />
      <div className="content">{props.children}</div>
      <input
        className="end"
        value={round(maxInput, 2)}
        type="number"
        name="max"
        onChange={(e) => setMaxInput(e.target.valueAsNumber)}
        onBlur={onSubmit}
        onKeyPress={handleEnter}
      />
    </div>
  );
}

// *******************************************************
// Tooltip
// *******************************************************

interface TooltipProps {
  value: number | null;
  percent: number | null;
}

function Tooltip(props: TooltipProps) {
  const tooltipCss = css`
    left: ${props.percent}%;
    position: absolute;
    margin-left: -11px;
    margin-top: -35px;
    padding: 10px;
  `;
  return (
    <div className="Tooltip" css={tooltipCss}>
      {props.value?.toFixed(2)}
    </div>
  );
}

// *******************************************************
// RAIL
// *******************************************************

const railCss = (theme: BifrostTheme) => css`
  position: absolute;
  width: 100%;
  height: 3px;
  transform: translate(0%, -50%);
  border-radius: 7px;
  cursor: pointer;
  background: ${theme.color.primary.light};
`;

const tooltipRailCss = css`
  position: absolute;
  width: 100%;
  height: 15px;
  transform: translate(0%, -50%);
  cursor: pointer;
  z-index: 20;
`;

interface SliderRailProps {
  activeHandleID: string;
  getRailProps: GetRailProps;
  getEventData: GetEventData;
}

function SliderRail({
  activeHandleID,
  getRailProps,
  getEventData,
}: SliderRailProps) {
  const [tooltipState, setTooltipState] = useState<TooltipProps>({
    value: null,
    percent: null,
  });

  /**
   * Update the tooltip value
   */
  const onMouseMove = useCallback((e: MouseEvent) => {
    setTooltipState(
      activeHandleID ? { value: null, percent: null } : getEventData(e)
    );
  }, []);
  /**
   * Attach events for tooltip
   */
  function onMouseEnter() {
    document.addEventListener('mousemove', onMouseMove);
  }
  /**
   * Remove tooltip events
   */
  function onMouseLeave() {
    setTooltipState({ value: null, percent: null });
    document.removeEventListener('mousemove', onMouseMove);
  }

  return (
    <Fragment>
      <Tooltip {...tooltipState} />
      <div
        className="tooltip-rail"
        css={tooltipRailCss}
        {...getRailProps({
          onMouseEnter,
          onMouseLeave,
        })}
      />
      <div className="rail" css={railCss} />
    </Fragment>
  );
  // <div/>
}

// *******************************************************
// HANDLE COMPONENT
// *******************************************************

interface HandleProps {
  domain: [number, number];
  handle: SliderItem;
  disabled?: boolean;
  getHandleProps: GetHandleProps;
}

function Handle({
  domain: [min, max],
  handle: { id, value, percent },
  disabled = false,
  getHandleProps,
}: HandleProps) {
  const handleCss = (theme: BifrostTheme) => css`
    left: ${percent}%;
    position: absolute;
    transform: translate(-50%, -50%);
    z-index: 2;
    width: 15px;
    height: 15px;

    border-radius: 50%;
    border: 1px solid ${theme.color.primary.dark};
    box-shadow: ${theme.shadow.handle};
    background-color: ${disabled
      ? theme.color.primary.light
      : theme.color.primary.standard};
  `;

  return (
    <div
      role="slider"
      aria-valuemin={min}
      aria-valuemax={max}
      aria-valuenow={value}
      css={handleCss}
      className="handle-2"
      {...getHandleProps(id)}
    />
  );
}

// *******************************************************
// TRACK COMPONENT
// *******************************************************

interface TrackProps {
  source: SliderItem;
  target: SliderItem;
  getTrackProps: GetTrackProps;
  disabled?: boolean;
}

function Track({
  source,
  target,
  getTrackProps,
  disabled = false,
}: TrackProps) {
  return (
    <div
      className="track"
      css={(theme) => css`
        position: absolute;
        transform: translate(0%, -50%);
        height: 7px;
        z-index: 1;
        background-color: ${theme.color.primary.light};
        border-radius: 7px;
        cursor: pointer;
        left: ${source.percent}%;
        width: ${target.percent - source.percent}%;
      `}
      {...getTrackProps()}
    />
  );
}
