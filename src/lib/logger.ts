import winston from 'winston';
import 'winston-daily-rotate-file';
import path from 'path';

// Define log format
const logFormat = winston.format.combine(
  winston.format.timestamp({ format: 'YYYY-MM-DD HH:mm:ss' }),
  winston.format.printf(
    (info) => `[${info.timestamp}] ${info.level.toUpperCase()}: ${info.message}`
  )
);

// Create a rotating file transport
const fileRotateTransport = new winston.transports.DailyRotateFile({
  filename: 'logs/ssr-%DATE%.log',
  datePattern: 'YYYY-MM-DD',
  maxFiles: '14d', // Keep logs for 14 days
  maxSize: '20m',  // Rotate if file exceeds 20MB
});

// Create the logger
export const logger = winston.createLogger({
  level: 'info',
  format: logFormat,
  transports: [
    fileRotateTransport,
    // Keep console output for development visibility
    new winston.transports.Console({
      format: winston.format.combine(
        winston.format.colorize(),
        logFormat
      )
    })
  ],
});
