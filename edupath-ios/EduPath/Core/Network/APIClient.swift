import Foundation

/// HTTP API client with automatic token injection and refresh.
actor APIClient {
    private let baseURL: URL
    private let session: URLSession
    private let tokenStorage: TokenStorage

    /// Timeout matches backend nginx config (30s).
    private static let defaultTimeout: TimeInterval = 30

    init(
        baseURL: URL,
        session: URLSession = .shared,
        tokenStorage: TokenStorage
    ) {
        self.baseURL = baseURL
        self.session = session
        self.tokenStorage = tokenStorage
    }

    /// GET request with optional query parameters.
    func get<T: Decodable>(
        _ path: String,
        queryItems: [URLQueryItem]? = nil
    ) async throws -> T {
        let request = try buildRequest(path: path, method: "GET", queryItems: queryItems)
        return try await execute(request)
    }

    /// POST request with JSON body.
    func post<T: Decodable, B: Encodable>(
        _ path: String,
        body: B
    ) async throws -> T {
        var request = try buildRequest(path: path, method: "POST")
        request.httpBody = try JSONEncoder().encode(body)
        request.setValue("application/json", forHTTPHeaderField: "Content-Type")
        return try await execute(request)
    }

    /// PATCH request with JSON body.
    func patch<T: Decodable, B: Encodable>(
        _ path: String,
        body: B
    ) async throws -> T {
        var request = try buildRequest(path: path, method: "PATCH")
        request.httpBody = try JSONEncoder().encode(body)
        request.setValue("application/json", forHTTPHeaderField: "Content-Type")
        return try await execute(request)
    }

    // MARK: - Private

    private func buildRequest(
        path: String,
        method: String,
        queryItems: [URLQueryItem]? = nil
    ) throws -> URLRequest {
        var components = URLComponents(url: baseURL.appendingPathComponent(path), resolvingAgainstBaseURL: true)
        components?.queryItems = queryItems

        guard let url = components?.url else {
            throw APIError.invalidURL
        }

        var request = URLRequest(url: url)
        request.httpMethod = method
        request.timeoutInterval = Self.defaultTimeout

        // Inject auth token if available
        if let token = tokenStorage.accessToken {
            request.setValue("Bearer \(token)", forHTTPHeaderField: "Authorization")
        }

        return request
    }

    private func execute<T: Decodable>(_ request: URLRequest) async throws -> T {
        let (data, response) = try await session.data(for: request)

        guard let httpResponse = response as? HTTPURLResponse else {
            throw APIError.invalidResponse
        }

        // Handle 401 - token may need refresh
        if httpResponse.statusCode == 401 {
            throw APIError.unauthorized
        }

        guard (200...299).contains(httpResponse.statusCode) else {
            let message = try? JSONDecoder().decode(ErrorResponse.self, from: data)
            throw APIError.serverError(
                statusCode: httpResponse.statusCode,
                message: message?.detail ?? "Request failed"
            )
        }

        let decoder = JSONDecoder()
        decoder.keyDecodingStrategy = .convertFromSnakeCase
        decoder.dateDecodingStrategy = .iso8601

        return try decoder.decode(T.self, from: data)
    }
}

/// API errors.
enum APIError: LocalizedError {
    case invalidURL
    case invalidResponse
    case unauthorized
    case serverError(statusCode: Int, message: String)

    var errorDescription: String? {
        switch self {
        case .invalidURL: return "Invalid URL"
        case .invalidResponse: return "Invalid server response"
        case .unauthorized: return "Authentication required"
        case .serverError(_, let message): return message
        }
    }
}

/// Generic error response from backend.
private struct ErrorResponse: Decodable {
    let detail: String
}
