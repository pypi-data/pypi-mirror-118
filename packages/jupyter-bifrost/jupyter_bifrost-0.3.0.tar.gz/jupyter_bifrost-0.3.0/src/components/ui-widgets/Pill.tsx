/**@jsx jsx */
import { jsx, css } from '@emotion/react';

const pillCss = css`
  display: inline-block;
  list-style: none;
  padding: 5px;
  background: #dedede;
  border-radius: 7px;
  border: 1px solid transparent;
  transition: border-color 0.5s;
  width: min-content;
  margin: 7px;

  &:hover {
    border-color: gray;
  }

  .content-wrapper {
    display: flex;
    align-items: center;
  }

  button {
    margin: 0 10px;
  }
`;

const activeCss = (theme: any) => css`
  background-color: ${theme.color.primary.dark};
  color: white;
  svg {
    color: white;
  }
`;

interface PillProps extends React.LiHTMLAttributes<HTMLLIElement> {
  children?: React.ReactNode;
  onClick?: () => void;
  active?: boolean;
}

export default function Pill({
  active,
  children,
  onClick,
  ...rest
}: PillProps) {
  return (
    <li css={[pillCss, active && activeCss]} onClick={onClick} {...rest}>
      <div className="content-wrapper">{children}</div>
    </li>
  );
}
