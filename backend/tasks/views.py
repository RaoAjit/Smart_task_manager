from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status

from .serializers import TaskInputSerializer, TaskOutputSerializer
from .scoring import balanced_score
from .utils import detect_cycles

class AnalyzeTasksView(APIView):
    def post(self, request):
        data = request.data
        print(data)
        if isinstance(data, dict):
              data = [data]
        serializer = TaskInputSerializer(data=request.data, many=True)
        serializer.is_valid(raise_exception=True)

        tasks = serializer.validated_data

        if detect_cycles(tasks):
            return Response(
                {"error": "Circular dependency detected"},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Compute scores
        results = []
        for task in tasks:
            score, explanation = balanced_score(task, tasks)
            results.append({**task, "score": score, "explanation": explanation})

        # Sort by score desc
        results.sort(key=lambda t: t["score"], reverse=True)

        output = TaskOutputSerializer(results, many=True)
        return Response(output.data, status=200)


class SuggestTasksView(APIView):
    def get(self, request):
        sample = request.query_params.get("tasks")
        if not sample:
            return Response({"error": "Provide tasks in ?tasks=[]"}, status=400)

        import json
        tasks = json.loads(sample)

        if detect_cycles(tasks):
            return Response({"error": "Circular dependency detected"}, status=400)

        results = []
        for t in tasks:
            score, explanation = balanced_score(t, tasks)
            results.append({**t, "score": score, "explanation": explanation})

        results.sort(key=lambda t: t["score"], reverse=True)
        top3 = results[:3]

        return Response(top3, status=200)