import Foundation
import Vision
import AppKit

// Usage: swift ocr.swift image.png
// Prints one line per recognized text observation: "x0 y0 x1 y1\ttext" (coords normalized, origin top-left)
let path = CommandLine.arguments[1]
guard let img = NSImage(contentsOfFile: path),
      let cg = img.cgImage(forProposedRect: nil, context: nil, hints: nil) else {
    fputs("cannot load \(path)\n", stderr); exit(1)
}
let req = VNRecognizeTextRequest()
req.recognitionLevel = .accurate
req.recognitionLanguages = ["fr-FR"]
req.usesLanguageCorrection = true
let handler = VNImageRequestHandler(cgImage: cg, options: [:])
try handler.perform([req])
var rows: [(Double, Double, Double, Double, String)] = []
for obs in req.results ?? [] {
    guard let c = obs.topCandidates(1).first else { continue }
    let b = obs.boundingBox
    rows.append((Double(b.minX), Double(1 - b.maxY), Double(b.maxX), Double(1 - b.minY), c.string))
}
rows.sort { ($0.1, $0.0) < ($1.1, $1.0) }
for r in rows {
    print(String(format: "%.3f %.3f %.3f %.3f\t", r.0, r.1, r.2, r.3) + r.4)
}
