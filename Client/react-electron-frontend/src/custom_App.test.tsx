import React from 'react';
import { render, screen } from '@testing-library/react';
import Custom_App from './custom_App';

test('renders learn react link', () => {
  render(<Custom_App />);
  const linkElement = screen.getByText(/learn react/i);
  expect(linkElement).toBeInTheDocument();
});
