import Foundation

/// Course repository implementation using API client.
final class CourseRepositoryImpl: CourseRepository {
    private let api: APIClient

    init(api: APIClient) {
        self.api = api
    }

    func getCourses(
        category: String?,
        search: String?,
        isFree: Bool?
    ) async throws -> [Course] {
        var queryItems: [URLQueryItem] = []

        if let category = category {
            queryItems.append(URLQueryItem(name: "category__slug", value: category))
        }
        if let search = search {
            queryItems.append(URLQueryItem(name: "search", value: search))
        }
        if let isFree = isFree {
            queryItems.append(URLQueryItem(name: "is_free", value: String(isFree)))
        }

        let response: PaginatedResponse<CourseDTO> = try await api.get(
            "courses/api/v1/courses/",
            queryItems: queryItems.isEmpty ? nil : queryItems
        )

        return response.results.map { $0.toDomain() }
    }

    func getCourse(slug: String) async throws -> Course? {
        let dto: CourseDTO = try await api.get("courses/api/v1/courses/\(slug)/")
        return dto.toDomain()
    }

    func getFeaturedCourses() async throws -> [Course] {
        let dtos: [CourseDTO] = try await api.get("courses/api/v1/courses/featured/")
        return dtos.map { $0.toDomain() }
    }

    func getFreeCourses() async throws -> [Course] {
        let dtos: [CourseDTO] = try await api.get("courses/api/v1/courses/free/")
        return dtos.map { $0.toDomain() }
    }

    func getCategories() async throws -> [Category] {
        let response: PaginatedResponse<CategoryDTO> = try await api.get("courses/api/v1/categories/")
        return response.results.map { $0.toDomain() }
    }

    func getInstructors() async throws -> [Instructor] {
        let response: PaginatedResponse<InstructorDTO> = try await api.get("courses/api/v1/instructors/")
        return response.results.map { $0.toDomain() }
    }

    func getReviews(courseId: Int) async throws -> [Review] {
        let response: PaginatedResponse<ReviewDTO> = try await api.get(
            "courses/api/v1/reviews/",
            queryItems: [URLQueryItem(name: "course", value: String(courseId))]
        )
        return response.results.map { $0.toDomain() }
    }

    func submitReview(courseId: Int, rating: Int, description: String) async throws -> Review {
        let request = ReviewCreateRequest(course: courseId, rating: rating, desc: description)
        let dto: ReviewDTO = try await api.post("courses/api/v1/reviews/", body: request)
        return dto.toDomain()
    }
}
